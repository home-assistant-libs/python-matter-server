"""OTA implementation for the Matter Server."""

import asyncio
import json
from logging import LoggerAdapter
from pathlib import Path

from matter_server.common.models import UpdateSource
from matter_server.server.ota import dcl

MatterProduct = tuple[int, int]

_local_updates: dict[MatterProduct, dict[int | str, dict]] = {}


async def load_local_updates(ota_provider_dir: Path) -> None:
    """Load updates from locally stored json files."""

    def _load_update(ota_provider_dir: Path) -> None:
        if not ota_provider_dir.exists():
            return
        for update_file in ota_provider_dir.glob("*.json"):
            with open(update_file) as f:
                update = json.load(f)
                model_version = update["modelVersion"]
                model_key = (model_version["vid"], model_version["pid"])
                update_dict = _local_updates.get(model_key, {})
                # Store by string or integer, this allows update by both
                update_dict[model_version["softwareVersion"]] = model_version
                update_dict[model_version["softwareVersionString"]] = model_version
                _local_updates[model_key] = update_dict

    await asyncio.get_running_loop().run_in_executor(
        None, _load_update, ota_provider_dir
    )


async def check_for_update(
    logger: LoggerAdapter,
    vid: int,
    pid: int,
    current_software_version: int,
    requested_software_version: int | str | None = None,
) -> tuple[UpdateSource, dict] | tuple[None, None]:
    """Check for software updates."""
    if local_updates := _local_updates.get((vid, pid)):
        logger.info("Local updates found for this device")
        if requested_software_version is None:
            # Use integer version to reliably determine absolute latest version
            versions = filter(
                lambda version: isinstance(version, int), local_updates.keys()
            )
            return UpdateSource.LOCAL, local_updates[max(versions)]
        if requested_software_version in local_updates:
            return UpdateSource.LOCAL, local_updates[requested_software_version]

    if dcl_update := await dcl.check_for_update(
        logger, vid, pid, current_software_version, requested_software_version
    ):
        return UpdateSource.MAIN_NET_DCL, dcl_update
    return None, None
