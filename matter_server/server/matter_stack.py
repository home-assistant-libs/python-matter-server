import logging

from chip.ChipDeviceCtrl import ChipDeviceController
from chip.ChipStack import ChipStack
import chip.logging
import chip.native

_LOGGER = logging.getLogger(__name__)


class MatterStack:

    # To track if wifi credentials set this session.
    wifi_cred_set = False
    device_controller: ChipDeviceController
    certificate_authority_manager = None

    def __init__(self, storage_path):
        _LOGGER.info("Setup CHIP Controller Server")
        chip.native.Init()
        chip.logging.RedirectToPythonLogging()
        self.stack = ChipStack(
            persistentStoragePath=storage_path, enableServerInteractions=True
        )
        self.certificate_authority_manager = (
            chip.CertificateAuthority.CertificateAuthorityManager(
                self.stack, self.stack.GetStorageManager()
            )
        )

        self.certificate_authority_manager.LoadAuthoritiesFromStorage()

        if len(self.certificate_authority_manager.activeCaList) == 0:
            ca = self.certificate_authority_manager.NewCertificateAuthority()
            ca.NewFabricAdmin(vendorId=0xFFF1, fabricId=1)
        elif len(self.certificate_authority_manager.activeCaList[0].adminList) == 0:
            self.certificate_authority_manager.activeCaList[0].NewFabricAdmin(
                vendorId=0xFFF1, fabricId=1
            )

        self.device_controller = (
            self.certificate_authority_manager.activeCaList[0]
            .adminList[0]
            .NewController()
        )
        _LOGGER.info("CHIP Controller Stack initialized")
        self.fabric_id = self.device_controller.fabricId
        self.compressed_fabric_id = self.device_controller.GetCompressedFabricId()

    def shutdown(self):
        _LOGGER.info("Shutdown CHIP Controller Server")
        self.device_controller.Shutdown()
        self.stack.Shutdown()
