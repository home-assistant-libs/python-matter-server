import logging

from chip.ChipDeviceCtrl import ChipDeviceController
from chip.ChipStack import ChipStack
from chip.FabricAdmin import FabricAdmin
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
        self.fabric_admin = FabricAdmin()
        self.device_controller = self.fabric_admin.NewController()
        _LOGGER.info("CHIP Controller Stack initialized")
        self.fabric_id = self.device_controller.GetFabricId()
        self.compressed_fabric_id = self.device_controller.GetCompressedFabricId()

    def shutdown(self):
        _LOGGER.info("Shutdown CHIP Controller Server")
        self.device_controller.Shutdown()
        self.stack.Shutdown()
