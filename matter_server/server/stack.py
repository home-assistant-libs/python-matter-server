"""Implementation of a Websocket-based Matter proxy (using CHIP SDK)."""

import logging
from typing import TYPE_CHECKING

from chip.ChipStack import ChipStack
import chip.logging
import chip.native
from chip.ChipDeviceCtrl import ChipDeviceController

from matter_server.server.device_controller import MatterDeviceController

if TYPE_CHECKING:
    from chip.CertificateAuthority import CertificateAuthorityManager


DEFAULT_VENDOR_ID = 0xFFF1
DEFAULT_FABRIC_ID = 1


class MatterStack:
    """Class that holds the Matter/CHIP Stack."""

    def __init__(
        self,
        storage_path: str,
        vendor_id: int = DEFAULT_VENDOR_ID,
        fabric_id: int = DEFAULT_FABRIC_ID,
    ) -> None:
        """Initialize Matter Stack."""
        self.logger = logging.getLogger(__name__)
        self.logger.info("Initializing CHIP/Matter Controller Stack...")
        self.logger.debug("Using storage path: %s", storage_path)
        chip.native.Init()
        chip.logging.RedirectToPythonLogging()

        self.stack = ChipStack(
            persistentStoragePath=storage_path, enableServerInteractions=True
        )

        # Initialize Certificate Authoritity Manager
        # yeah the import is a bit weird just to prevent a circular import in the underlying SDK
        self.certificate_authority_manager: CertificateAuthorityManager = (
            chip.CertificateAuthority.CertificateAuthorityManager(
                self.stack, self.stack.GetStorageManager()
            )
        )
        self.certificate_authority_manager.LoadAuthoritiesFromStorage()

        # Get Certificate Authority (create new if we do not yet have one)
        if len(self.certificate_authority_manager.activeCaList) == 0:
            ca = self.certificate_authority_manager.NewCertificateAuthority()
            ca.NewFabricAdmin(vendorId=0xFFF1, fabricId=1)
        else:
            ca = self.certificate_authority_manager.activeCaList[0]

        # Get Fabric Admin (create new if we do not yet have one)
        if len(self.certificate_authority_manager.activeCaList[0].adminList) == 0:
            self.fabric_admin = self.certificate_authority_manager.activeCaList[
                0
            ].NewFabricAdmin(vendorId=vendor_id, fabricId=fabric_id)
        else:
            self.fabric_admin = ca.adminList[0]

        # Initialize our (intermediate) device controller which keeps track
        # of Matter devices and their subscriptions.
        self.device_controller = MatterDeviceController(self)
        self.logger.info("CHIP Controller Stack initialized.")
        self.fabric_id = self.device_controller.fabricId
        self.compressed_fabric_id = self.device_controller.GetCompressedFabricId()

    def shutdown(self) -> None:
        """ "Shutdown Matter Stack."""
        self.logger.info("Shutdown CHIP Controller Server")
        self.device_controller.Shutdown()
        self.stack.Shutdown()
