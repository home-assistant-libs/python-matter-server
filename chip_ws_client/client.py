import json
import logging
from dataclasses import asdict, dataclass, is_dataclass
from functools import partial

import aiohttp
from chip_ws_common.wsmsg import WSEncoder, WSMethodMessage

_LOGGER = logging.getLogger(__name__)

import chip.clusters.Objects as Clusters


class CHIPControllerClient:
    _ws: aiohttp.ClientWebSocketResponse

    def __init__(self, url):
        self._url = url
        pass

    async def setup(self):
        _LOGGER.info("Setup CHIP Controller Client")
        session = aiohttp.ClientSession()
        self._ws = await session.ws_connect(self._url)
        _LOGGER.info("WebSocket connected")

    async def send(self, msg: str):
        await self._ws.send_str(msg)

    async def send_toggle(self):
        await self.send_command(nodeid=4335, endpoint=1, payload=Clusters.OnOff.Commands.Toggle())

    async def send_move(self):
        await self.send_command(nodeid=4335, endpoint=1, payload=Clusters.ColorControl.Commands.MoveToHueAndSaturation(200,100,0,0,0))

    async def send_command(self, **args):
        for arg, value in args.items():
            # Add type information to dataclasses
            if is_dataclass(value):
                cmd_dict = asdict(value)
                cls = type(value)
                cmd_dict["_type"] = f"{cls.__module__}.{cls.__qualname__}"
                args[arg] = cmd_dict

        wscmd = WSMethodMessage(method="send_command", args=args)
        await self._ws.send_json(wscmd, dumps=partial(json.dumps, cls=WSEncoder))

    def shutdown(self):
        _LOGGER.info("Shutdown CHIP Controller Client")
        self._ws.close()
