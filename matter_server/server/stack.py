"""Implementation of a Websocket-based Matter proxy (using CHIP SDK)."""

import logging
import os
from typing import TYPE_CHECKING

import chip.CertificateAuthority
from chip.ChipStack import ChipStack
import chip.logging
from chip.logging import (
    ERROR_CATEGORY_DETAIL,
    ERROR_CATEGORY_ERROR,
    ERROR_CATEGORY_NONE,
    ERROR_CATEGORY_PROGRESS,
)
from chip.logging.library_handle import _GetLoggingLibraryHandle
from chip.logging.types import LogRedirectCallback_t
import chip.native

if TYPE_CHECKING:
    from chip.FabricAdmin import FabricAdmin

    from .server import MatterServer

_LOGGER = logging.getLogger(__name__)

CHIP_ERROR = logging.ERROR - 1
CHIP_PROGRESS = logging.INFO - 1
CHIP_DETAIL = logging.DEBUG - 1
CHIP_AUTOMATION = logging.DEBUG - 2

_category_num: int = 4


@LogRedirectCallback_t  # type: ignore[misc]
def _redirect_to_python_logging(
    category: int, raw_module: bytes, raw_message: bytes
) -> None:
    module = raw_module.decode("utf-8")
    message = raw_message.decode("utf-8")

    logger = logging.getLogger(f"chip.native.{module}")

    # All logs are expected to have some reasonable category. This treats
    # unknown/None as critical.
    level = logging.CRITICAL

    if category == ERROR_CATEGORY_ERROR:
        level = CHIP_ERROR
    elif category == ERROR_CATEGORY_PROGRESS:
        level = CHIP_PROGRESS
    elif category == ERROR_CATEGORY_DETAIL:
        level = CHIP_DETAIL
    elif category == 4:  # TODO: Add automation level to upstream Python bindings
        level = CHIP_AUTOMATION

    logger.log(level, "%s", message)


def init_logging(category: str) -> None:
    """Initialize Matter SDK logging. Filter by category."""

    _LOGGER.info("Initializing CHIP/Matter Logging...")
    global _category_num  # pylint: disable=global-statement  # noqa: PLW0603
    _category_num = ERROR_CATEGORY_NONE
    if category == "ERROR":
        _category_num = ERROR_CATEGORY_ERROR
    elif category == "PROGRESS":
        _category_num = ERROR_CATEGORY_PROGRESS
    elif category == "DETAIL":
        _category_num = ERROR_CATEGORY_DETAIL
    elif category == "AUTOMATION":
        _category_num = 4

    logging.addLevelName(CHIP_ERROR, "CHIP_ERROR")
    logging.addLevelName(CHIP_PROGRESS, "CHIP_PROGRESS")
    logging.addLevelName(CHIP_DETAIL, "CHIP_DETAIL")
    logging.addLevelName(CHIP_AUTOMATION, "CHIP_AUTOMATION")
    logging.getLogger("chip.native").setLevel(CHIP_AUTOMATION)

    # We can't setup logging here yet as the stack needs to be
    # initialized first!


class MatterStack:
    """Class that holds the Matter/CHIP Stack."""

    def __init__(
        self,
        server: "MatterServer",
    ) -> None:
        """Initialize Matter Stack."""
        self.logger = logging.getLogger(__name__)
        self.logger.info("Initializing CHIP/Matter Controller Stack...")
        storage_file = os.path.join(server.storage_path, "chip.json")
        self.logger.debug("Using storage file: %s", storage_file)
        chip.native.Init()

        # Initialize logging after stack init!
        # See: https://github.com/project-chip/connectedhomeip/issues/20233
        handle = _GetLoggingLibraryHandle()
        handle.pychip_logging_set_callback(_redirect_to_python_logging)

        # Handle log level selection on SDK level
        chip.logging.SetLogFilter(_category_num)

        self._chip_stack = ChipStack(
            persistentStoragePath=storage_file,
            installDefaultLogHandler=False,
            enableServerInteractions=False,
        )

        # Initialize Certificate Authority Manager
        # yeah this is a bit weird just to prevent a circular import in the underlying SDK
        self.certificate_authority_manager: chip.CertificateAuthority.CertificateAuthorityManager = chip.CertificateAuthority.CertificateAuthorityManager(
            chipStack=self._chip_stack
        )
        self.certificate_authority_manager.LoadAuthoritiesFromStorage()

        # Get Certificate Authority (create new if we do not yet have one)
        if len(self.certificate_authority_manager.activeCaList) == 0:
            cert_auth = self.certificate_authority_manager.NewCertificateAuthority()
            cert_auth.maximizeCertChains = False
        else:
            cert_auth = self.certificate_authority_manager.activeCaList[0]

        # Get Fabric Admin (create new if we do not yet have one)
        for admin in cert_auth.adminList:
            if (
                admin.vendorId == server.vendor_id
                and admin.fabricId == server.fabric_id
            ):
                self.fabric_admin: FabricAdmin = admin
                break
        else:
            self.fabric_admin = cert_auth.NewFabricAdmin(
                vendorId=server.vendor_id, fabricId=server.fabric_id
            )

        self.logger.info("CHIP Controller Stack initialized.")

    def shutdown(self) -> None:
        """Stop/Shutdown Matter Stack."""
        self.logger.info("Shutting down the Matter stack...")
        # NOTE that this will abruptly end the python process!
        self.certificate_authority_manager.Shutdown()
        self._chip_stack.Shutdown()
