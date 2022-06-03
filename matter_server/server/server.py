from __future__ import annotations
import asyncio
import json
import logging
from dataclasses import asdict, is_dataclass
from functools import partial
from pprint import pformat
from typing import TYPE_CHECKING
import weakref

from aiohttp.web import WebSocketResponse, Application, run_app, WSMsgType

from aiohttp import WSCloseCode, WSMsgType
from chip.exceptions import ChipStackError

from ..common.json_utils import CHIPJSONDecoder, CHIPJSONEncoder

if TYPE_CHECKING:
    from .matter_stack import MatterStack


def create_success_response(message, result):
    return {
        "type": "result",
        "success": True,
        "messageId": message["messageId"],
        "result": result,
    }


def create_error_response(message, code):
    return {
        "type": "result",
        "success": False,
        "messageId": message["messageId"],
        "errorCode": code,
    }


def create_event_response(subscriptionId, payload):
    return {
        "type": "event",
        "subscriptionId": subscriptionId,
        "payload": payload,
    }


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
        self.logger.info("New connection...")
        self.ws = WebSocketResponse()
        await self.ws.prepare(self.request)

        await self.ws.send_json(
            {
                "driverVersion": 0,
                "serverVersion": 0,
                "minSchemaVersion": 1,
                "maxSchemaVersion": 1,
            }
        )

        self.logger.info("Websocket connection ready")

        event_task = asyncio.create_task(self.server.stack.get_next_event())
        ws_task = asyncio.create_task(self.ws.receive())
        while True:
            done, _ = await asyncio.wait(
                [event_task, ws_task], return_when=asyncio.FIRST_COMPLETED
            )

            if ws_task in done:
                msg = ws_task.result()
                if msg.type in (
                    WSMsgType.CLOSE,
                    WSMsgType.CLOSING,
                    WSMsgType.CLOSED,
                ):
                    break

                try:
                    await self._handle_message(msg)
                except Exception:
                    self.logger.exception("Error handling message: %s", msg)
                ws_task = asyncio.create_task(self.ws.receive())

            if event_task in done:
                event = event_task.result()
                try:
                    await self._handle_event(event)
                except Exception:
                    self.logger.exception("Error handling event: %s", event)
                event_task = asyncio.create_task(self.server.stack.get_next_event())

        self.logger.info("Websocket connection closed")
        return self.ws

    async def _handle_event(self, payload):
        await self.send_msg(create_event_response(payload["SubscriptionId"], payload))

    async def _handle_message(self, msg: dict):
        if msg.type != WSMsgType.TEXT:
            self.logger.debug("Ignoring %s", msg)
            return

        self.logger.info("Received: %s", msg.data)
        msg = json.loads(msg.data, cls=CHIPJSONDecoder)
        self.logger.info("Deserialized message: %s", msg)
        if msg["command"] == "start_listening":
            await self.send_msg(
                create_success_response(
                    msg,
                    {
                        "state": {
                            "device_controller": {
                                # Enum chip.ChipDeviceCtrl.DCState
                                "state": {
                                    0: "NOT_INITIALIZED",
                                    1: "IDLE",
                                    2: "BLE_READY",
                                    3: "RENDEZVOUS_ONGOING",
                                    4: "RENDEZVOUS_CONNECTED",
                                }.get(
                                    self.server.stack.device_controller.state, "UNKNOWN"
                                )
                            }
                        }
                    },
                )
            )
            return

        # See if it's an instance method
        instance, _, command = msg["command"].partition(".")
        if not instance or not command:
            await self.send_msg(create_error_response(msg, "INVALID_COMMAND"))
            self.logger.warning("Unknown command: %s", msg["command"])
            return

        if instance == "device_controller":
            method = None
            args = msg["args"]

            if command == "CommissionWithCode" and not self.server.stack.wifi_cred_set:
                self.logger.warning("Received commissioning without Wi-Fi set")

            if command == "Read" and isinstance(args.get("attributes"), list):
                converted_attributes = []
                for attribute in args["attributes"]:
                    if isinstance(attribute, list):
                        converted_attributes.append(tuple(attribute))
                    else:
                        converted_attributes.append(attribute)

                args["attributes"] = converted_attributes

            if command[0] != "_":
                method = self.server.stack.get_method(command)
            if not method:
                await self.send_msg(create_error_response(msg, "INVALID_COMMAND"))
                self.logger.error("Unknown command: %s", msg["command"])
                return

            try:
                raw_result = method(**args)

                if asyncio.iscoroutine(raw_result):
                    raw_result = await raw_result

                if is_dataclass(raw_result):
                    result = asdict(raw_result)
                    cls = type(raw_result)
                    result["_type"] = f"{cls.__module__}.{cls.__qualname__}"

                    # asdict doesn't convert dictionary keys that are dataclasses.
                    # Rest already processed by `asdict`
                    def convert_class_keys(val):
                        if isinstance(val, dict):
                            return {
                                k.__name__
                                if isinstance(k, type)
                                else k: convert_class_keys(v)
                                for k, v in val.items()
                            }
                        if isinstance(val, list):
                            return [convert_class_keys(v) for v in val]
                        return val

                    result = convert_class_keys(result)

                else:
                    result = raw_result

                if command == "SetWiFiCredentials" and result == 0:
                    self.server.stack.wifi_cred_set = True

                await self.send_msg(create_success_response(msg, result))
            except ChipStackError as ex:
                await self.send_msg(create_error_response(msg, str(ex)))
            except Exception:
                self.logger.exception("Error calling method: %s", msg["command"])
                await self.send_msg(create_error_response(msg, "UNKNOWN"))

        else:
            self.logger.warning("Unknown command: %s", msg["command"])
            await self.send_msg(create_error_response(msg, "INVALID_COMMAND"))
