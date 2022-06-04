import asyncio
import logging
import typing

from chip.ChipDeviceCtrl import ChipDeviceController
from chip.ChipStack import ChipStack
from chip.FabricAdmin import FabricAdmin
from chip.clusters import Attribute, ClusterObjects
import chip.logging
import chip.native

_LOGGER = logging.getLogger(__name__)


class MatterStack:

    # To track if wifi credentials set this session.
    wifi_cred_set = False
    device_controller: ChipDeviceController

    def __init__(self, storage_path):
        _LOGGER.info("Setup CHIP Controller Server")
        chip.native.GetLibraryHandle()
        chip.logging.RedirectToPythonLogging()
        self.stack = ChipStack(persistentStoragePath=storage_path)
        self.fabricAdmin = FabricAdmin()
        self.device_controller = self.fabricAdmin.NewController()
        _LOGGER.info("CHIP Controller Stack initialized")

    def shutdown(self):
        _LOGGER.info("Shutdown CHIP Controller Server")
        self.device_controller.Shutdown()
        self.stack.Shutdown()
