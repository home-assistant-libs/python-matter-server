import json
import logging
from dataclasses import asdict, dataclass
from functools import partial

import aiohttp
from chip_ws_common.wsmsg import WSCommandMessage, WSEncoder

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
        await self.send_command(Clusters.OnOff.Commands.Toggle())

    async def send_move(self):
        await self.send_command(Clusters.ColorControl.Commands.MoveToHueAndSaturation(200,100,0,0,0))

    async def send_command(self, cmd: Clusters.ClusterCommand):
        cmd_dict = asdict(cmd)
        cls = type(cmd)
        cmd_dict["_type"] = f"{cls.__module__}.{cls.__qualname__}"
        wscmd = WSCommandMessage(command="test", args={ "val": cmd_dict })
        await self._ws.send_json(wscmd, dumps=partial(json.dumps, cls=WSEncoder))

    def shutdown(self):
        _LOGGER.info("Shutdown CHIP Controller Client")
        self._ws.close()
