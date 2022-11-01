"""Logic to handle a client connected over websockets."""
from __future__ import annotations

import asyncio
import logging
from typing import TYPE_CHECKING, Awaitable, Coroutine

from aiohttp import web

from matter_server.common.model.server_information import (
    FullServerState,
    ServerInfo,
    VersionInfo,
)

if TYPE_CHECKING:
    from .stack import MatterStack

import asyncio
from concurrent import futures
from contextlib import suppress
import json
import logging
from typing import TYPE_CHECKING, Any, Callable, Final
import weakref

from aiohttp import WSMsgType, web
import async_timeout

from ..common.json_utils import CHIPJSONDecoder, CHIPJSONEncoder
from ..common.model.message import (
    CommandMessage,
    ErrorCode,
    ErrorResultMessage,
)

if TYPE_CHECKING:
    from .server import MatterServer

MAX_PENDING_MSG = 512
CANCELLATION_ERRORS: Final = (asyncio.CancelledError, futures.CancelledError)


class WebSocketLogAdapter(logging.LoggerAdapter):
    """Add connection id to websocket log messages."""

    def process(self, msg: str, kwargs: Any) -> tuple[str, Any]:
        """Add connid to websocket log messages."""
        return f'[{self.extra["connid"]}] {msg}', kwargs


class WebsocketCommands(dict):
    """Small helper to register commands."""

    def register(self, command: str):
        """Decorate a command handler."""

        def decorator(func: Callable[..., Coroutine[Any, Any, Any]]):
            self[command] = func
            return func

        return decorator


COMMANDS = WebsocketCommands()


class WebsocketClientHandler:
    """Handle an active websocket client connection."""

    def __init__(self, server: MatterServer, request: web.Request) -> None:
        """Initialize an active connection."""
        self.server = server
        self.request = request
        self.wsock = web.WebSocketResponse(heartbeat=55)
        self._to_write: asyncio.Queue = asyncio.Queue(maxsize=MAX_PENDING_MSG)
        self._handle_task: asyncio.Task | None = None
        self._writer_task: asyncio.Task | None = None
        self._logger = WebSocketLogAdapter(server.logger, {"connid": id(self)})
        self._unsub_callback: Callable | None = None

    async def disconnect(self) -> None:
        """Disconnect client."""
        self._cancel()
        await self._writer_task

    async def handle_client(self) -> web.WebSocketResponse:
        """Handle a websocket response."""
        request = self.request
        wsock = self.wsock
        try:
            async with async_timeout.timeout(10):
                await wsock.prepare(request)
        except asyncio.TimeoutError:
            self._logger.warning("Timeout preparing request from %s", request.remote)
            return wsock

        self._logger.debug("Connected from %s", request.remote)
        self._handle_task = asyncio.current_task()

        self._writer_task = asyncio.create_task(self._writer())

        # send server(version) info when client connects
        self._send_message(self.server.get_info())

        disconnect_warn = None

        try:
            while not wsock.closed:
                msg = await wsock.receive()

                if msg.type in (WSMsgType.CLOSE, WSMsgType.CLOSING):
                    break

                if msg.type != WSMsgType.TEXT:
                    disconnect_warn = "Received non-Text message."
                    break

                self._logger.debug("Received: %s", msg.data)

                try:
                    command_msg = json.loads(msg.data, cls=CHIPJSONDecoder)
                except ValueError:
                    disconnect_warn = "Received invalid JSON."
                    break

                self._logger.info("Deserialized message: %s", command_msg)

                if not isinstance(command_msg, CommandMessage):
                    disconnect_warn = "Did not receive a CommandMessage."
                    break

                self._logger.debug("Received %s", command_msg)
                self._handle_command(command_msg)

        except asyncio.CancelledError:
            self._logger.info("Connection closed by client")

        except Exception:  # pylint: disable=broad-except
            self._logger.exception("Unexpected error inside websocket API")

        finally:
            # Handle connection shutting down.
            if self._unsub_callback:
                self._logger.debug("Unsubscribed from events")
                self._unsub_callback()

            try:
                self._to_write.put_nowait(None)
                # Make sure all error messages are written before closing
                await self._writer_task
                await wsock.close()
            except asyncio.QueueFull:  # can be raised by put_nowait
                self._writer_task.cancel()

            finally:
                if disconnect_warn is None:
                    self._logger.debug("Disconnected")
                else:
                    self._logger.warning("Disconnected: %s", disconnect_warn)

        return wsock

    def _handle_command(self, msg: CommandMessage) -> None:
        """Handle an incoming command from the client."""
        handler = COMMANDS.get(msg.command)

        if handler is None:
            self._send_message(
                ErrorResultMessage(
                    msg.messageId,
                    ErrorCode.INVALID_COMMAND,
                    f"Invalid command: {msg.command}",
                )
            )
            self._logger.warning("Invalid command: %s", msg.command)
            return

        # schedule task to handle the command
        self.server.loop.create_task(self._run_handler(handler, msg))

    @COMMANDS.register("server.state")
    async def _handle_state(self) -> FullServerState:
        """Send full server state to connected client."""
        return self.server.info

    @COMMANDS.register("server.listen")
    async def _handle_start_listening(self) -> None:
        """Dump full state and subscribe client to all events."""

    async def _run_handler(self, handler, msg: CommandMessage) -> None:
        try:
            result = await handler(self, **msg.args)
            self._send_message(SuccessResultMessage(msg.messageId, True))
        except ChipStackError as err:
            self._send_message(
                ErrorResultMessage(msg.messageId, ErrorCode.STACK_ERROR, str(err))
            )
        except Exception as err:  # pylint: disable=broad-except
            self._logger.exception("Error handling message: %s", msg)
            self._send_message(
                ErrorResultMessage(msg.messageId, ErrorCode.UNKNOWN_ERROR, str(err))
            )

    async def _writer(self) -> None:
        """Write outgoing messages."""
        # Exceptions if Socket disconnected or cancelled by connection handler
        with suppress(RuntimeError, ConnectionResetError, *CANCELLATION_ERRORS):
            while not self.wsock.closed:
                if (process := await self._to_write.get()) is None:
                    break

                if not isinstance(process, str):
                    message: str = process()
                else:
                    message = process
                self._logger.debug("Sending %s", message)
                await self.wsock.send_str(message)

    def _send_message(self, message: str | dict[str, Any] | Callable[[], str]) -> None:
        """Send a message to the client.

        Closes connection if the client is not reading the messages.

        Async friendly.
        """
        message = json.dumps(message, cls=CHIPJSONEncoder)

        try:
            self._to_write.put_nowait(message)
        except asyncio.QueueFull:
            self._logger.error(
                "Client exceeded max pending messages: %s", MAX_PENDING_MSG
            )

            self._cancel()

    def _cancel(self) -> None:
        """Cancel the connection."""
        if self._handle_task is not None:
            self._handle_task.cancel()
        if self._writer_task is not None:
            self._writer_task.cancel()
