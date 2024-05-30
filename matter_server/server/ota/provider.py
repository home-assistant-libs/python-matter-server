"""Handling Matter OTA provider."""

from __future__ import annotations

import asyncio
from base64 import b64encode
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
import functools
import hashlib
import json
import logging
from pathlib import Path
import secrets
from typing import TYPE_CHECKING, Final, cast
from urllib.parse import unquote, urlparse

from aiohttp import ClientError, ClientSession
from aiohttp.client_exceptions import InvalidURL
from chip.clusters import Attribute, Objects as Clusters, Types
from chip.discovery import FilterType
from chip.exceptions import ChipStackError
from chip.interaction_model import Status

from matter_server.common.errors import UpdateError
from matter_server.common.helpers.util import dataclass_from_dict

if TYPE_CHECKING:
    from asyncio.subprocess import Process

    from chip.native import PyChipError

    from matter_server.server.sdk import ChipDeviceControllerWrapper

LOGGER = logging.getLogger(__name__)

DEFAULT_UPDATES_PATH: Final[Path] = Path("updates")

DEFAULT_OTA_PROVIDER_NODE_ID = 999900

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


@dataclass
class DeviceSoftwareVersionModel:  # pylint: disable=C0103
    """Device Software Version Model for OTA Provider JSON descriptor file."""

    vendorId: int
    productId: int
    softwareVersion: int
    softwareVersionString: str
    cDVersionNumber: int
    softwareVersionValid: bool
    minApplicableSoftwareVersion: int
    maxApplicableSoftwareVersion: int
    otaURL: str


@dataclass
class OtaProviderImageList:  # pylint: disable=C0103
    """Update File for OTA Provider JSON descriptor file."""

    otaProviderDiscriminator: int
    otaProviderPasscode: int
    otaProviderNodeId: int | None
    deviceSoftwareVersionModel: list[DeviceSoftwareVersionModel]


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
        self._ota_provider_image_list_file: Path = ota_provider_dir / "updates.json"
        self._ota_provider_image_list: OtaProviderImageList | None = None
        self._ota_provider_proc: Process | None = None
        self._ota_provider_task: asyncio.Task | None = None
        self._ota_provider_lock: asyncio.Lock = asyncio.Lock()
        self._ota_target_node_id: int | None = None

    async def initialize(self) -> None:
        """Initialize OTA Provider."""

        loop = asyncio.get_event_loop()

        # Take existence of image list file as indicator if we need to initialize the
        # OTA Provider.
        if not await loop.run_in_executor(
            None, self._ota_provider_image_list_file.exists
        ):
            await loop.run_in_executor(
                None, functools.partial(DEFAULT_UPDATES_PATH.mkdir, exist_ok=True)
            )

            # Initialize with random data. Node ID will get written once paired by
            # device controller.
            self._ota_provider_image_list = OtaProviderImageList(
                otaProviderDiscriminator=secrets.randbelow(2**12),
                otaProviderPasscode=secrets.randbelow(2**21),
                otaProviderNodeId=None,
                deviceSoftwareVersionModel=[],
            )
        else:

            def _read_update_json(
                update_json_path: Path,
            ) -> None | OtaProviderImageList:
                with open(update_json_path, "r") as json_file:
                    data = json.load(json_file)
                    return dataclass_from_dict(OtaProviderImageList, data)

            self._ota_provider_image_list = await loop.run_in_executor(
                None, _read_update_json, self._ota_provider_image_list_file
            )

    def _get_ota_provider_image_list(self) -> OtaProviderImageList:
        if self._ota_provider_image_list is None:
            raise RuntimeError("OTA provider image list not initialized.")
        return self._ota_provider_image_list

    async def _commission_ota_provider(
        self,
        passcode: int,
        descriminator: int,
        chip_device_controller: ChipDeviceControllerWrapper,
    ) -> int:
        """Commissions the OTA Provider, returns node ID of the commissioned provider."""

        res: PyChipError = await chip_device_controller.commission_on_network(
            DEFAULT_OTA_PROVIDER_NODE_ID,
            passcode,
            # TODO: Filtering by long discriminator seems broken
            disc_filter_type=FilterType.LONG_DISCRIMINATOR,
            disc_filter=descriminator,
        )
        if not res.is_success:
            await self.stop()
            raise UpdateError(
                f"Failed to commission OTA Provider App: SDK Error {res.code}"
            )

        LOGGER.info(
            "OTA Provider App commissioned with node id %d.",
            DEFAULT_OTA_PROVIDER_NODE_ID,
        )

        # Adjust ACL of OTA Requestor such that Node peer-to-peer communication
        # is allowed.
        try:
            read_result = cast(
                Attribute.AsyncReadTransaction.ReadResponse,
                await chip_device_controller.read_attribute(
                    DEFAULT_OTA_PROVIDER_NODE_ID,
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
                    DEFAULT_OTA_PROVIDER_NODE_ID,
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

        return DEFAULT_OTA_PROVIDER_NODE_ID

    def _write_ota_provider_image_list_json(
        self,
        ota_provider_image_list_file: Path,
        ota_provider_image_list: OtaProviderImageList,
    ) -> None:
        update_file_dict = asdict(ota_provider_image_list)
        with open(ota_provider_image_list_file, "w") as json_file:
            json.dump(update_file_dict, json_file, indent=4)

    async def start_update(
        self, chip_device_controller: ChipDeviceControllerWrapper, node_id: int
    ) -> None:
        """Start the OTA Provider and trigger the update."""

        # Don't hold the response
        if self._ota_provider_lock.locked():
            raise UpdateError(
                "OTA Provider already running. Only one update at a time possible."
            )

        await self._ota_provider_lock.acquire()

        self._ota_target_node_id = node_id

        loop = asyncio.get_running_loop()
        image_list = self._get_ota_provider_image_list()
        await loop.run_in_executor(
            None,
            self._write_ota_provider_image_list_json,
            self._ota_provider_image_list_file,
            image_list,
        )

        ota_provider_cmd = [
            "chip-ota-provider-app",
            "--discriminator",
            str(image_list.otaProviderDiscriminator),
            "--passcode",
            str(image_list.otaProviderPasscode),
            "--secured-device-port",
            "5565",
            "--KVS",
            str(self._ota_provider_dir / "chip_kvs_ota_provider"),
            "--otaImageList",
            str(self._ota_provider_image_list_file),
        ]

        timestamp = datetime.now(tz=UTC).strftime("%Y%m%d_%H%M%S")
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

            # Commission and prepare OTA Provider if not initialized yet.
            # Use "ota_provider_node_id" to indicate if OTA Provider is setup or not.
            if image_list.otaProviderNodeId is None:
                LOGGER.info("Commission and initialize OTA Provider")
                image_list.otaProviderNodeId = await self._commission_ota_provider(
                    image_list.otaProviderPasscode,
                    image_list.otaProviderDiscriminator,
                    chip_device_controller,
                )

            # Notify update node about the availability of the OTA Provider. It will query
            # the OTA provider and start the update.
            try:
                await chip_device_controller.send_command(
                    node_id,
                    endpoint_id=0,
                    command=Clusters.OtaSoftwareUpdateRequestor.Commands.AnnounceOTAProvider(
                        providerNodeID=image_list.otaProviderNodeId,
                        vendorID=self._vendor_id,
                        announcementReason=Clusters.OtaSoftwareUpdateRequestor.Enums.AnnouncementReasonEnum.kUpdateAvailable,
                        endpoint=ExternalOtaProvider.ENDPOINT_ID,
                    ),
                )
            except ChipStackError as ex:
                raise UpdateError(
                    "Error while announcing OTA Provider to node."
                ) from ex
        except UpdateError as ex:
            # On error, make sure we stop the OTA Provider.
            await self.stop()
            raise ex

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

    async def add_update(self, update_desc: dict, ota_file: Path) -> None:
        """Add update to the OTA provider."""

        local_ota_url = str(ota_file)
        image_list = self._get_ota_provider_image_list()
        for i, device_software in enumerate(image_list.deviceSoftwareVersionModel):
            if device_software.otaURL == local_ota_url:
                LOGGER.debug("Device software entry exists already, replacing!")
                del image_list.deviceSoftwareVersionModel[i]

        # Convert to OTA Requestor descriptor file
        new_device_software = DeviceSoftwareVersionModel(
            vendorId=update_desc["vid"],
            productId=update_desc["pid"],
            softwareVersion=update_desc["softwareVersion"],
            softwareVersionString=update_desc["softwareVersionString"],
            cDVersionNumber=update_desc["cdVersionNumber"],
            softwareVersionValid=update_desc["softwareVersionValid"],
            minApplicableSoftwareVersion=update_desc["minApplicableSoftwareVersion"],
            maxApplicableSoftwareVersion=update_desc["maxApplicableSoftwareVersion"],
            otaURL=local_ota_url,
        )
        image_list.deviceSoftwareVersionModel.append(new_device_software)

    async def download_update(self, update_desc: dict) -> None:
        """Download update file from OTA Path and add it to the OTA provider."""

        url = update_desc["otaUrl"]
        parsed_url = urlparse(url)
        file_name = unquote(Path(parsed_url.path).name)

        loop = asyncio.get_running_loop()
        await loop.run_in_executor(
            None, functools.partial(DEFAULT_UPDATES_PATH.mkdir, exist_ok=True)
        )

        file_path = DEFAULT_UPDATES_PATH / file_name

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
                    DEFAULT_UPDATES_PATH,
                )

        except (InvalidURL, ClientError, TimeoutError) as err:
            LOGGER.error(
                "Fetching software version failed: error %s", err, exc_info=err
            )
            raise UpdateError("Fetching software version failed") from err

        await self.add_update(update_desc, file_path)

    async def check_update_state(
        self,
        node_id: int,
        update_state: Clusters.OtaSoftwareUpdateRequestor.Enums.UpdateStateEnum,
    ) -> None:
        """
        Check the update state of a node and take appropriate action.

        Args:
            node_id: The ID of the node.
            update_state: The update state of the node.
        """

        if self._ota_target_node_id is None:
            return

        if self._ota_target_node_id != node_id:
            return

        # Update state of target node changed, check if update is done.
        if (
            update_state
            == Clusters.OtaSoftwareUpdateRequestor.Enums.UpdateStateEnum.kIdle
        ):
            LOGGER.info("Update of node %d done.", node_id)
            await self.stop()
            self._ota_target_node_id = None
            self._ota_provider_lock.release()
