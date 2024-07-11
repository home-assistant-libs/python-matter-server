"""Handling Matter OTA provider."""

from __future__ import annotations

import asyncio
from base64 import b64encode
from datetime import UTC, datetime
import functools
import hashlib
import logging
from pathlib import Path
import secrets
from typing import TYPE_CHECKING, Any, Final, cast
from urllib.parse import unquote, urlparse

from aiohttp import ClientError, ClientSession
from aiohttp.client_exceptions import InvalidURL
from chip.clusters import Attribute, Objects as Clusters, Types
from chip.discovery import FilterType
from chip.exceptions import ChipStackError
from chip.interaction_model import Status

from matter_server.common.errors import UpdateError
from matter_server.common.helpers.util import (
    create_attribute_path_from_attribute,
)

if TYPE_CHECKING:
    from asyncio.subprocess import Process

    from chip.native import PyChipError

    from matter_server.server.sdk import ChipDeviceControllerWrapper

LOGGER = logging.getLogger(__name__)

DEFAULT_OTA_PROVIDER_NODE_ID: Final[int] = 990000

OTA_SOFTWARE_UPDATE_REQUESTOR_UPDATE_STATE_ATTRIBUTE_PATH = (
    create_attribute_path_from_attribute(
        0, Clusters.OtaSoftwareUpdateRequestor.Attributes.UpdateState
    )
)

# From Matter SDK src/app/ota_image_tool.py
CHECHKSUM_TYPES: Final[dict[int, str]] = {
    1: "sha256",
    2: "sha256_128",
    3: "sha256_120",
    4: "sha256_96",
    5: "sha256_64",
    6: "sha256_32",
    7: "sha384",
    8: "sha512",
    9: "sha3_224",
    10: "sha3_256",
    11: "sha3_384",
    12: "sha3_512",
}


class ExternalOtaProvider:
    """Class handling Matter OTA Provider.

    The OTA Provider class implements a Matter OTA (over-the-air) update provider
    for devices.
    """

    ENDPOINT_ID: Final[int] = 0

    def __init__(self, vendor_id: int, ota_provider_dir: Path) -> None:
        """Initialize the OTA provider."""
        self._vendor_id: int = vendor_id
        self._ota_provider_dir: Path = ota_provider_dir
        self._ota_file_path: Path | None = None
        self._ota_provider_proc: Process | None = None
        self._ota_provider_task: asyncio.Task | None = None
        self._ota_done: asyncio.Event = asyncio.Event()
        self._ota_target_node_id: int | None = None

    async def initialize(self) -> None:
        """Initialize OTA Provider."""

        loop = asyncio.get_event_loop()

        await loop.run_in_executor(
            None, functools.partial(self._ota_provider_dir.mkdir, exist_ok=True)
        )

    async def _commission_ota_provider(
        self,
        chip_device_controller: ChipDeviceControllerWrapper,
        passcode: int,
        discriminator: int,
        ota_provider_node_id: int,
    ) -> None:
        """Commissions the OTA Provider, returns node ID of the commissioned provider."""

        res: PyChipError = await chip_device_controller.commission_on_network(
            ota_provider_node_id,
            passcode,
            # TODO: Filtering by long discriminator seems broken
            disc_filter_type=FilterType.LONG_DISCRIMINATOR,
            disc_filter=discriminator,
        )
        if not res.is_success:
            await self.stop()
            raise UpdateError(
                f"Failed to commission OTA Provider App: SDK Error {res.code}"
            )

        LOGGER.info(
            "OTA Provider App commissioned with node id %d.",
            ota_provider_node_id,
        )

        # Adjust ACL of OTA Requestor such that Node peer-to-peer communication
        # is allowed.
        try:
            read_result = cast(
                Attribute.AsyncReadTransaction.ReadResponse,
                await chip_device_controller.read_attribute(
                    ota_provider_node_id,
                    [(0, Clusters.AccessControl.Attributes.Acl)],
                ),
            )
            acl_list = cast(
                list,
                read_result.attributes[0][Clusters.AccessControl][
                    Clusters.AccessControl.Attributes.Acl
                ],
            )

            # Add new ACL entry...
            acl_list.append(
                Clusters.AccessControl.Structs.AccessControlEntryStruct(
                    fabricIndex=1,
                    privilege=Clusters.AccessControl.Enums.AccessControlEntryPrivilegeEnum.kOperate,
                    authMode=Clusters.AccessControl.Enums.AccessControlEntryAuthModeEnum.kCase,
                    subjects=Types.NullValue,
                    targets=[
                        Clusters.AccessControl.Structs.AccessControlTargetStruct(
                            cluster=Clusters.OtaSoftwareUpdateProvider.id,
                            endpoint=0,
                            deviceType=Types.NullValue,
                        )
                    ],
                )
            )

            # And write. This is persistent, so only need to be done after we commissioned
            # the OTA Provider App.
            write_result: Attribute.AttributeWriteResult = (
                await chip_device_controller.write_attribute(
                    ota_provider_node_id,
                    [(0, Clusters.AccessControl.Attributes.Acl(acl_list))],
                )
            )
            if write_result[0].Status != Status.Success:
                logging.error(
                    "Failed writing adjusted OTA Provider App ACL: Status %s.",
                    str(write_result[0].Status),
                )
                await self.stop()
                raise UpdateError("Error while setting up OTA Provider.")
        except ChipStackError as ex:
            logging.exception("Failed adjusting OTA Provider App ACL.", exc_info=ex)
            await self.stop()
            raise UpdateError("Error while setting up OTA Provider.") from ex

    async def start_update(
        self, chip_device_controller: ChipDeviceControllerWrapper, node_id: int
    ) -> None:
        """Start the OTA Provider and trigger the update."""

        self._ota_target_node_id = node_id

        loop = asyncio.get_running_loop()

        ota_provider_passcode = secrets.randbelow(2**21)
        ota_provider_discriminator = secrets.randbelow(2**12)

        timestamp = datetime.now(tz=UTC).strftime("%Y%m%d_%H%M%S")
        ota_provider_cmd = [
            "chip-ota-provider-app",
            "--passcode",
            str(ota_provider_passcode),
            "--discriminator",
            str(ota_provider_discriminator),
            "--secured-device-port",
            "0",
            "--KVS",
            str(self._ota_provider_dir / f"chip_kvs_ota_provider_{timestamp}"),
            "--filepath",
            str(self._ota_file_path),
        ]

        log_file_path = self._ota_provider_dir / f"ota_provider_{timestamp}.log"

        log_file = await loop.run_in_executor(None, log_file_path.open, "w")

        try:
            LOGGER.info("Starting OTA Provider")
            self._ota_provider_proc = await asyncio.create_subprocess_exec(
                *ota_provider_cmd, stdout=log_file, stderr=log_file
            )

            self._ota_provider_task = loop.create_task(
                self._ota_provider_proc.communicate()
            )

            # Commission and prepare ephemeral OTA Provider
            LOGGER.info("Commission and initialize OTA Provider")
            ota_provider_node_id = (
                DEFAULT_OTA_PROVIDER_NODE_ID + self._ota_target_node_id
            )
            await self._commission_ota_provider(
                chip_device_controller,
                ota_provider_passcode,
                ota_provider_discriminator,
                ota_provider_node_id,
            )

            # Notify update node about the availability of the OTA Provider. It will query
            # the OTA provider and start the update.
            try:
                await chip_device_controller.send_command(
                    node_id,
                    endpoint_id=0,
                    command=Clusters.OtaSoftwareUpdateRequestor.Commands.AnnounceOTAProvider(
                        providerNodeID=ota_provider_node_id,
                        vendorID=self._vendor_id,
                        announcementReason=Clusters.OtaSoftwareUpdateRequestor.Enums.AnnouncementReasonEnum.kUpdateAvailable,
                        endpoint=ExternalOtaProvider.ENDPOINT_ID,
                    ),
                )
            except ChipStackError as ex:
                raise UpdateError(
                    "Error while announcing OTA Provider to node."
                ) from ex

            await self._ota_done.wait()
        finally:
            await self.stop()
            self._ota_target_node_id = None

    async def _reset(self) -> None:
        """Reset the OTA Provider App state."""

        def _remove_update_data(ota_provider_dir: Path) -> None:
            for path in ota_provider_dir.iterdir():
                if not path.is_dir():
                    path.unlink()

        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, _remove_update_data, self._ota_provider_dir)

        await self.initialize()

    async def stop(self) -> None:
        """Stop the OTA Provider."""
        if self._ota_provider_proc:
            LOGGER.info("Terminating OTA Provider")
            loop = asyncio.get_event_loop()
            try:
                await loop.run_in_executor(None, self._ota_provider_proc.terminate)
            except ProcessLookupError as ex:
                LOGGER.warning("Stopping OTA Provider failed with error:", exc_info=ex)
        if self._ota_provider_task:
            await self._ota_provider_task
        self._ota_provider_proc = None
        self._ota_provider_task = None

    async def download_update(self, update_desc: dict) -> None:
        """Download update file from OTA Path and add it to the OTA provider."""

        url = update_desc["otaUrl"]
        parsed_url = urlparse(url)
        file_name = unquote(Path(parsed_url.path).name)

        loop = asyncio.get_running_loop()

        file_path = self._ota_provider_dir / file_name

        try:
            checksum_alg = None
            if (
                "otaChecksum" in update_desc
                and "otaChecksumType" in update_desc
                and update_desc["otaChecksumType"] in CHECHKSUM_TYPES
            ):
                checksum_alg = hashlib.new(
                    CHECHKSUM_TYPES[update_desc["otaChecksumType"]]
                )
            else:
                LOGGER.warning(
                    "No OTA checksum type or not supported, OTA will not be checked."
                )

            async with ClientSession(raise_for_status=True) as session:
                # fetch the paa certificates list
                LOGGER.debug("Download update from '%s'.", url)
                async with session.get(url) as response:
                    with file_path.open("wb") as f:
                        while True:
                            chunk = await response.content.read(4048)
                            if not chunk:
                                break
                            await loop.run_in_executor(None, f.write, chunk)
                            if checksum_alg:
                                checksum_alg.update(chunk)

                # Download finished, check checksum if necessary
                if checksum_alg:
                    checksum = b64encode(checksum_alg.digest()).decode("ascii")
                    if checksum != update_desc["otaChecksum"]:
                        LOGGER.error(
                            "Checksum mismatch for file '%s', expected: %s, got: %s",
                            file_name,
                            update_desc["otaChecksum"],
                            checksum,
                        )
                        await loop.run_in_executor(None, file_path.unlink)
                        raise UpdateError("Checksum mismatch!")

                LOGGER.info(
                    "Update file '%s' downloaded to '%s'",
                    file_name,
                    self._ota_provider_dir,
                )

        except (InvalidURL, ClientError, TimeoutError) as err:
            LOGGER.error(
                "Fetching software version failed: error %s", err, exc_info=err
            )
            raise UpdateError("Fetching software version failed") from err

        self._ota_file_path = file_path

    async def check_update_state(
        self,
        path: Attribute.AttributePath,
        old_value: Any,
        new_value: Any,
    ) -> None:
        """Check the update state of a node and take appropriate action."""

        LOGGER.info("Update state changed: %s, %s %s", str(path), old_value, new_value)
        if str(path) != OTA_SOFTWARE_UPDATE_REQUESTOR_UPDATE_STATE_ATTRIBUTE_PATH:
            return

        update_state = cast(
            Clusters.OtaSoftwareUpdateRequestor.Enums.UpdateStateEnum, new_value
        )

        # Update state of target node changed, check if update is done.
        if (
            update_state
            == Clusters.OtaSoftwareUpdateRequestor.Enums.UpdateStateEnum.kIdle
        ):
            LOGGER.info(
                "Node %d update state idle, assuming done.", self._ota_target_node_id
            )
            self._ota_done.set()
