import json
import logging

import chip.clusters.Objects as Clusters
import chip.FabricAdmin
import chip.logging
import chip.native
import coloredlogs
from chip.ChipStack import *
from chip.tlv import float32, uint
from chip_ws_common.wsmsg import WSDecoder

_LOGGER = logging.getLogger(__name__)


class CHIPControllerServer:
    def __init__(self):
        pass

    def setup(self):
        _LOGGER.info("Setup CHIP Controller Server")
        chip.native.GetLibraryHandle()
        chip.logging.RedirectToPythonLogging()
        coloredlogs.install(level=logging.INFO)
        self._stack = ChipStack(persistentStoragePath="/tmp/repl-storage.json")

        self._fabricAdmin = chip.FabricAdmin.FabricAdmin()

        self._devController = self._fabricAdmin.NewController()
        _LOGGER.info("CHIP Controller Stack initialized")

    def shutdown(self):
        _LOGGER.info("Shutdown CHIP Controller Server")
        self._devController.Shutdown()
        self._stack.Shutdown()

    async def send_command(self, nodeid: int, endpoint: int, payload: Clusters.ClusterCommand, responseType=None, timedRequestTimeoutMs: int = None):
        _LOGGER.info("Sending command to node id %d, endpoint %d: %s", nodeid, endpoint, payload)
        await self._devController.SendCommand(nodeid, endpoint, payload)

    async def new_message(self, msgstr: str):
        _LOGGER.info(msgstr)
        msg = json.loads(msgstr, cls=WSDecoder)
        print(msg)
        if msg["method"] == "send_command":
            await self.send_command(**msg["args"])

