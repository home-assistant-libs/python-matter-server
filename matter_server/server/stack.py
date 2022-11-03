"""Implementation of a Websocket-based Matter proxy (using CHIP SDK)."""

import asyncio
import logging
from typing import TYPE_CHECKING

from chip.ChipStack import ChipStack
import chip.logging
import chip.native

if TYPE_CHECKING:
    from chip.CertificateAuthority import CertificateAuthorityManager

    from .server import MatterServer


class MatterStack:
    """Class that holds the Matter/CHIP Stack."""

    def __init__(
        self,
        server: MatterServer,
    ) -> None:
        """Initialize Matter Stack."""
        self.logger = logging.getLogger(__name__)
        self.logger.info("Initializing CHIP/Matter Controller Stack...")
        self.logger.debug("Using storage path: %s", server.storage_path)
        chip.native.Init()
        chip.logging.RedirectToPythonLogging()

        self.stack = ChipStack(
            persistentStoragePath=server.storage_path, enableServerInteractions=True
        )

        # Initialize Certificate Authoritity Manager
        # yeah this is a bit weird just to prevent a circular import in the underlying SDK
        self.certificate_authority_manager: CertificateAuthorityManager = (
            chip.CertificateAuthority.CertificateAuthorityManager(
                self.stack, self.stack.GetStorageManager()
            )
        )
        self.certificate_authority_manager.LoadAuthoritiesFromStorage()

        # Get Certificate Authority (create new if we do not yet have one)
        if len(self.certificate_authority_manager.activeCaList) == 0:
            ca = self.certificate_authority_manager.NewCertificateAuthority()
        else:
            ca = self.certificate_authority_manager.activeCaList[0]

        # Get Fabric Admin (create new if we do not yet have one)
        for admin in ca.adminList:
            if (
                admin.vendorId == server.vendor_id
                and admin.fabricId == server.fabric_id
            ):
                self.fabric_admin = admin
                break
        else:
            self.fabric_admin = ca.NewFabricAdmin(
                vendorId=server.vendor_id, fabricId=server.fabric_id
            )

        self.logger.info("CHIP Controller Stack initialized.")

    def shutdown(self) -> None:
        """Stop/Shutdown Matter Stack."""
        self.logger.info("Shutting down the Matter stack...")
        # NOTE that this will abruptly end the python process!
        self.stack.Shutdown()
