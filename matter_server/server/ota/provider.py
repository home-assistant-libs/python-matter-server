"""Handling Matter OTA provider."""

import asyncio
from dataclasses import asdict, dataclass
import functools
import json
import logging
from pathlib import Path
import secrets
from typing import TYPE_CHECKING, Final
from urllib.parse import unquote, urlparse

from aiohttp import ClientError, ClientSession

from matter_server.common.helpers.util import dataclass_from_dict

if TYPE_CHECKING:
    from asyncio.subprocess import Process

LOGGER = logging.getLogger(__name__)

DEFAULT_UPDATES_PATH: Final[Path] = Path("updates")


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

    def __init__(self, ota_provider_dir: Path) -> None:
        """Initialize the OTA provider."""
        self._ota_provider_dir: Path = ota_provider_dir
        self._ota_provider_image_list_file: Path = ota_provider_dir / "updates.json"
        self._ota_provider_image_list: OtaProviderImageList | None = None
        self._ota_provider_proc: Process | None = None
        self._ota_provider_task: asyncio.Task | None = None

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

    def get_node_id(self) -> int | None:
        """Get Node ID of the OTA Provider App."""

        return self._get_ota_provider_image_list().otaProviderNodeId

    def get_descriminator(self) -> int:
        """Return OTA Provider App discriminator."""

        return self._get_ota_provider_image_list().otaProviderDiscriminator

    def get_passcode(self) -> int:
        """Return OTA Provider App passcode."""

        return self._get_ota_provider_image_list().otaProviderPasscode

    def set_node_id(self, node_id: int) -> None:
        """Set Node ID of the OTA Provider App."""

        self._get_ota_provider_image_list().otaProviderNodeId = node_id

    async def _start_ota_provider(self) -> None:
        def _write_ota_provider_image_list_json(
            ota_provider_image_list_file: Path,
            ota_provider_image_list: OtaProviderImageList,
        ) -> None:
            update_file_dict = asdict(ota_provider_image_list)
            with open(ota_provider_image_list_file, "w") as json_file:
                json.dump(update_file_dict, json_file, indent=4)

        loop = asyncio.get_running_loop()
        await loop.run_in_executor(
            None,
            _write_ota_provider_image_list_json,
            self._ota_provider_image_list_file,
            self._get_ota_provider_image_list(),
        )

        ota_provider_cmd = [
            "chip-ota-provider-app",
            "--discriminator",
            str(self._get_ota_provider_image_list().otaProviderDiscriminator),
            "--passcode",
            str(self._get_ota_provider_image_list().otaProviderPasscode),
            "--secured-device-port",
            "5565",
            "--KVS",
            str(self._ota_provider_dir / "chip_kvs_ota_provider"),
            "--otaImageList",
            str(self._ota_provider_image_list_file),
        ]

        LOGGER.info("Starting OTA Provider")
        self._ota_provider_proc = await asyncio.create_subprocess_exec(
            *ota_provider_cmd
        )

    def start(self) -> None:
        """Start the OTA Provider."""

        loop = asyncio.get_event_loop()
        self._ota_provider_task = loop.create_task(self._start_ota_provider())

    async def reset(self) -> None:
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

    async def add_update(self, update_desc: dict, ota_file: Path) -> None:
        """Add update to the OTA provider."""

        local_ota_url = str(ota_file)
        for i, device_software in enumerate(
            self._get_ota_provider_image_list().deviceSoftwareVersionModel
        ):
            if device_software.otaURL == local_ota_url:
                LOGGER.debug("Device software entry exists already, replacing!")
                del self._get_ota_provider_image_list().deviceSoftwareVersionModel[i]

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
        self._get_ota_provider_image_list().deviceSoftwareVersionModel.append(
            new_device_software
        )

    async def download_update(self, update_desc: dict) -> None:
        """Download update file from OTA Path and add it to the OTA provider."""

        url = update_desc["otaUrl"]
        parsed_url = urlparse(url)
        file_name = unquote(Path(parsed_url.path).name)

        loop = asyncio.get_running_loop()
        await loop.run_in_executor(
            None, functools.partial(DEFAULT_UPDATES_PATH.mkdir, exists_ok=True)
        )

        file_path = DEFAULT_UPDATES_PATH / file_name
        if await loop.run_in_executor(None, file_path.exists):
            LOGGER.info("File '%s' exists already, skipping download.", file_name)
            return

        try:
            async with ClientSession(raise_for_status=True) as session:
                # fetch the paa certificates list
                logging.debug("Download update from f{url}.")
                async with session.get(url) as response:
                    with file_path.open("wb") as f:
                        while True:
                            chunk = await response.content.read(4048)
                            if not chunk:
                                break
                            await loop.run_in_executor(None, f.write, chunk)

                # TODO: Check against otaChecksum

                LOGGER.info(
                    "File '%s' downloaded to '%s'", file_name, DEFAULT_UPDATES_PATH
                )

        except (ClientError, TimeoutError) as err:
            LOGGER.error(
                "Fetching software version failed: error %s", err, exc_info=err
            )

        await self.add_update(update_desc, file_path)
