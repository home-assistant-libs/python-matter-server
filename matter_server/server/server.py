from __future__ import annotations

import asyncio
import json
import logging
import weakref
from dataclasses import asdict, is_dataclass
from functools import partial
from pprint import pformat
from typing import TYPE_CHECKING

from aiohttp import WSCloseCode, WSMsgType
from aiohttp.web import Application, WebSocketResponse, WSMsgType, run_app
from chip.exceptions import ChipStackError
from matter_server.common.model.message import (CommandMessage,
                                                ErrorResultMessage, Message,
                                                SubscriptionReportMessage,
                                                SuccessResultMessage)
from matter_server.common.model.version import VersionInfo
from setuptools import Command

from ..common.json_utils import CHIPJSONDecoder, CHIPJSONEncoder

if TYPE_CHECKING:
    from .matter_stack import MatterStack


class MatterServer:
    """Serve Matter over WS."""

    def __init__(self, stack: MatterStack):
        self.stack = stack
        self.logger = logging.getLogger(__name__)
        self.app = Application()
        self.loop = asyncio.get_running_loop()
        self.clients = weakref.WeakSet()
        self.app.on_shutdown.append(self._handle_shutdown)

        self.app.router.add_route("GET", "/chip_ws", self._handle_chip_ws)

    async def _handle_chip_ws(self, request):
        connection = MatterServerClient(self, request)
        try:
            self.clients.add(connection)
            return await connection.handle_request()
        finally:
            self.clients.remove(connection)

    async def _handle_shutdown(self, app):
        for client in set(self.clients):
            await client.disconnect()

    def run(self, host, port):
        """Run the server."""
        run_app(self.app, host=host, port=port, loop=self.loop)


class MatterServerClient:

    ws: WebSocketResponse | None = None

    def __init__(self, server: MatterServer, request):
        self.server = server
        self.request = request
        self.logger = server.logger

    async def send_msg(self, msg):
        self.logger.info("Sending message: %s", pformat(msg))
        await self.ws.send_json(msg, dumps=partial(json.dumps, cls=CHIPJSONEncoder))

    async def disconnect(self):
        await self.ws.close(code=WSCloseCode.GOING_AWAY, message="Server shutdown")

    async def handle_request(self):
        self.logger.info("New Client connection...")
        self.ws = WebSocketResponse()
        await self.ws.prepare(self.request)

        await self.send_msg(VersionInfo(driver_version=0, server_version=0, min_schema_version=1, max_schema_version=1))

        self.logger.info("Websocket connection ready")

        sr_task = asyncio.create_task(self.server.stack.get_next_subscription_report())
        ws_task = asyncio.create_task(self.ws.receive())
        while True:
            done, _ = await asyncio.wait(
                [sr_task, ws_task], return_when=asyncio.FIRST_COMPLETED
            )

            if ws_task in done:
                msg = ws_task.result()
                if msg.type in (
                    WSMsgType.CLOSE,
                    WSMsgType.CLOSING,
                    WSMsgType.CLOSED,
                ):
                    break

                if msg.type != WSMsgType.TEXT:
                    self.logger.debug("Ignoring %s", msg)
                    continue

                try:
                    self.logger.info("Received: %s", msg.data)
                    msg = json.loads(msg.data, cls=CHIPJSONDecoder)
                    self.logger.info("Deserialized message: %s", msg)
                    if not isinstance(msg, CommandMessage):
                        self.logger.exception("Invalid Message received: %s", msg)
                        continue
                    await self._handle_message(msg)
                except Exception:
                    self.logger.exception("Error handling message: %s", msg)
                ws_task = asyncio.create_task(self.ws.receive())

            if sr_task in done:
                sr = sr_task.result()
                try:
                    await self._handle_subscription_report(sr)
                except Exception:
                    self.logger.exception("Error handling subscription report: %s", sr)
                sr_task = asyncio.create_task(self.server.stack.get_next_subscription_report())

        self.logger.info("Websocket connection closed")
        return self.ws

    async def _handle_subscription_report(self, payload):
        await self.send_msg(SubscriptionReportMessage(payload["SubscriptionId"], payload))

    async def _handle_message(self, msg: CommandMessage):
        # See if it's an instance method
        instance, _, command = msg.command.partition(".")
        if not instance or not command:
            await self.send_msg(ErrorResultMessage(msg.messageId, "INVALID_COMMAND"))
            self.logger.warning("Unknown command: %s", msg.command)
            return

        if instance == "device_controller":
            method = None

            if command == "CommissionWithCode" and not self.server.stack.wifi_cred_set:
                self.logger.warning("Received commissioning without Wi-Fi set")

            if command == "Read" and isinstance(msg.args.get("attributes"), list):
                converted_attributes = []
                for attribute in msg.args["attributes"]:
                    if isinstance(attribute, list):
                        converted_attributes.append(tuple(attribute))
                    else:
                        converted_attributes.append(attribute)

                msg.args["attributes"] = converted_attributes

            if command[0] != "_":
                method = self.server.stack.get_method(command)
            if not method:
                await self.send_msg(ErrorResultMessage(msg.messageId, "INVALID_COMMAND"))
                self.logger.error("Unknown command: %s", command)
                return

            try:
                result = method(**msg.args)

                if asyncio.iscoroutine(result):
                    result = await result

                if command == "SetWiFiCredentials" and result == 0:
                    self.server.stack.wifi_cred_set = True
                await self.send_msg(SuccessResultMessage(msg.messageId, result))
            except ChipStackError as ex:
                await self.send_msg(ErrorResultMessage(msg.messageId, str(ex)))
            except Exception:
                self.logger.exception("Error calling method: %s", command)
                await self.send_msg(ErrorResultMessage(msg.messageId, "UNKNOWN"))

        else:
            self.logger.warning("Unknown command: %s", command)
            await self.send_msg(ErrorResultMessage(msg.messageId, "INVALID_COMMAND"))
