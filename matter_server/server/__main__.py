import asyncio
import json
import logging
import os
import sys
from dataclasses import asdict, is_dataclass
from functools import partial
from pathlib import Path
from pprint import pformat
import weakref

import aiohttp
import aiohttp.web
from aiohttp import WSCloseCode, WSMsgType
from chip.exceptions import ChipStackError

from ..common.json_utils import CHIPJSONDecoder, CHIPJSONEncoder
from .server import CHIPControllerServer

logging.basicConfig(level=logging.WARN)
_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.DEBUG)

HOST = os.getenv("CHIP_WS_SERVER_HOST", "0.0.0.0")
PORT = int(os.getenv("CHIP_WS_SERVER_PORT", 8080))
STORAGE_PATH = os.getenv(
    "CHIP_WS_STORAGE", Path.joinpath(Path.home(), ".chip-storage/python-kv.json")
)


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


async def websocket_handler(request, server: CHIPControllerServer):
    _LOGGER.info("New connection...")
    ws = aiohttp.web.WebSocketResponse()
    await ws.prepare(request)

    request.app["websockets"].add(ws)

    try:
        await ws.send_json(
            {
                "driverVersion": 0,
                "serverVersion": 0,
                "minSchemaVersion": 1,
                "maxSchemaVersion": 1,
            }
        )

        _LOGGER.info("Websocket connection ready")

        async def send_msg(msg):
            _LOGGER.info("Sending message: %s", pformat(msg))
            await ws.send_json(msg, dumps=partial(json.dumps, cls=CHIPJSONEncoder))

        event_task = asyncio.create_task(server.get_next_event())
        ws_task = asyncio.create_task(ws.receive())
        while True:
            done, _ = await asyncio.wait(
                [event_task, ws_task], return_when=asyncio.FIRST_COMPLETED
            )

            if ws_task in done:
                msg = ws_task.result()
                if msg.type in (WSMsgType.CLOSE, WSMsgType.CLOSING, WSMsgType.CLOSED):
                    break

                try:
                    await handle_message(send_msg, server, msg)
                except Exception:
                    _LOGGER.exception("Error handling message: %s", msg)
                ws_task = asyncio.create_task(ws.receive())

            if event_task in done:
                event = event_task.result()
                try:
                    await handle_event(send_msg, event)
                except Exception:
                    _LOGGER.exception("Error handling event: %s", event)
                event_task = asyncio.create_task(server.get_next_event())
    finally:
        request.app["websockets"].discard(ws)

    _LOGGER.info("Websocket connection closed")
    return ws


async def handle_event(send_msg, payload):
    await send_msg(create_event_response(payload["SubscriptionId"], payload))


async def handle_message(send_msg, server: CHIPControllerServer, msg: dict):
    if msg.type != aiohttp.WSMsgType.TEXT:
        _LOGGER.debug("Ignoring %s", msg)
        return

    _LOGGER.info("Received: %s", msg.data)
    msg = json.loads(msg.data, cls=CHIPJSONDecoder)
    _LOGGER.info("Deserialized message: %s", msg)
    if msg["command"] == "start_listening":
        await send_msg(
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
                            }.get(server.device_controller.state, "UNKNOWN")
                        }
                    }
                },
            )
        )
        return

    # See if it's an instance method
    instance, _, command = msg["command"].partition(".")
    if not instance or not command:
        await send_msg(create_error_response(msg, "INVALID_COMMAND"))
        _LOGGER.warning("Unknown command: %s", msg["command"])
        return

    if instance == "device_controller":
        method = None
        args = msg["args"]

        if command == "CommissionWithCode" and not server.wifi_cred_set:
            _LOGGER.warning("Received commissioning without Wi-Fi set")

        if command == "Read" and isinstance(args.get("attributes"), list):
            converted_attributes = []
            for attribute in args["attributes"]:
                if isinstance(attribute, list):
                    converted_attributes.append(tuple(attribute))
                else:
                    converted_attributes.append(attribute)

            args["attributes"] = converted_attributes

        if command[0] != "_":
            method = server.get_method(command)
        if not method:
            await send_msg(create_error_response(msg, "INVALID_COMMAND"))
            _LOGGER.error("Unknown command: %s", msg["command"])
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
                server.wifi_cred_set = True

            await send_msg(create_success_response(msg, result))
        except ChipStackError as ex:
            await send_msg(create_error_response(msg, str(ex)))
        except Exception:
            _LOGGER.exception("Error calling method: %s", msg["command"])
            await send_msg(create_error_response(msg, "UNKNOWN"))

    else:
        _LOGGER.warning("Unknown command: %s", msg["command"])
        await send_msg(create_error_response(msg, "INVALID_COMMAND"))


def main() -> int:
    # Create asyncio loop early e.g. for asyncio.Queue creation
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    server = CHIPControllerServer()
    server.setup(STORAGE_PATH)
    app = aiohttp.web.Application()
    app["websockets"] = weakref.WeakSet()

    async def on_shutdown(app):
        for ws in set(app["websockets"]):
            await ws.close(code=WSCloseCode.GOING_AWAY, message="Server shutdown")

    app.on_shutdown.append(on_shutdown)

    app.router.add_route("GET", "/chip_ws", partial(websocket_handler, server=server))
    aiohttp.web.run_app(app, host=HOST, port=PORT, loop=loop)
    server.shutdown()


if __name__ == "__main__":
    sys.exit(main())
