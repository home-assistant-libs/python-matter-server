"""Handling Matter OTA provider."""

import asyncio
from dataclasses import asdict, dataclass
import functools
import json
import logging
from pathlib import Path
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
class UpdateFile:  # pylint: disable=C0103
    """Update File for OTA Provider JSON descriptor file."""

    deviceSoftwareVersionModel: list[DeviceSoftwareVersionModel]


class ExternalOtaProvider:
    """Class handling Matter OTA Provider.

    The OTA Provider class implements a Matter OTA (over-the-air) update provider
    for devices.
    """

    def __init__(self) -> None:
        """Initialize the OTA provider."""
        self._ota_provider_proc: Process | None = None
        self._ota_provider_task: asyncio.Task | None = None

    async def _start_ota_provider(self) -> None:
        # TODO: Randomize discriminator
        ota_provider_cmd = [
            "chip-ota-provider-app",
            "--discriminator",
            "22",
            "--secured-device-port",
            "5565",
            "--KVS",
            "/data/chip_kvs_provider",
            "--otaImageList",
            str(DEFAULT_UPDATES_PATH / "updates.json"),
        ]

        LOGGER.info("Starting OTA Provider")
        self._ota_provider_proc = await asyncio.create_subprocess_exec(
            *ota_provider_cmd
        )

    def start(self) -> None:
        """Start the OTA Provider."""

        loop = asyncio.get_event_loop()
        self._ota_provider_task = loop.create_task(self._start_ota_provider())

    async def stop(self) -> None:
        """Stop the OTA Provider."""
        if self._ota_provider_proc:
            LOGGER.info("Terminating OTA Provider")
            self._ota_provider_proc.terminate()
        if self._ota_provider_task:
            await self._ota_provider_task

    async def add_update(self, update_desc: dict, ota_file: Path) -> None:
        """Add update to the OTA provider."""

        update_json_path = DEFAULT_UPDATES_PATH / "updates.json"

        def _read_update_json(update_json_path: Path) -> None | UpdateFile:
            if not update_json_path.exists():
                return None

            with open(update_json_path, "r") as json_file:
                data = json.load(json_file)
                return dataclass_from_dict(UpdateFile, data)

        loop = asyncio.get_running_loop()
        update_file = await loop.run_in_executor(
            None, _read_update_json, update_json_path
        )

        if not update_file:
            update_file = UpdateFile(deviceSoftwareVersionModel=[])

        local_ota_url = str(ota_file)
        for i, device_software in enumerate(update_file.deviceSoftwareVersionModel):
            if device_software.otaURL == local_ota_url:
                LOGGER.debug("Device software entry exists already, replacing!")
                del update_file.deviceSoftwareVersionModel[i]

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
        update_file.deviceSoftwareVersionModel.append(new_device_software)

        def _write_update_json(update_json_path: Path, update_file: UpdateFile) -> None:
            update_file_dict = asdict(update_file)
            with open(update_json_path, "w") as json_file:
                json.dump(update_file_dict, json_file, indent=4)

        await loop.run_in_executor(
            None,
            _write_update_json,
            update_json_path,
            update_file,
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
