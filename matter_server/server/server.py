import logging

from chip.FabricAdmin import FabricAdmin
import chip.logging
import chip.native
import coloredlogs
from chip.ChipStack import ChipStack

_LOGGER = logging.getLogger(__name__)


class CHIPControllerServer:

    # To track if wifi credentials set this session.
    wifi_cred_set = False

    def __init__(self):
        pass

    def setup(self, storage_path):
        _LOGGER.info("Setup CHIP Controller Server")
        chip.native.GetLibraryHandle()
        chip.logging.RedirectToPythonLogging()
        coloredlogs.install(level=logging.INFO)
        self._stack = ChipStack(persistentStoragePath=storage_path)

        self._fabricAdmin = FabricAdmin()

        self.device_controller = self._fabricAdmin.NewController()
        _LOGGER.info("CHIP Controller Stack initialized")

    def shutdown(self):
        _LOGGER.info("Shutdown CHIP Controller Server")
        self.device_controller.Shutdown()
        self._stack.Shutdown()
