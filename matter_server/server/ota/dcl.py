"""Handle OTA software version endpoints of the DCL."""

import logging
from typing import Any, cast

from aiohttp import ClientError, ClientSession

from matter_server.server.helpers import DCL_PRODUCTION_URL

LOGGER = logging.getLogger(__name__)


async def _get_software_versions(vid: int, pid: int) -> Any:
    """Check DCL if there are updates available for a particular node."""
    async with ClientSession(raise_for_status=True) as http_session:
        # fetch the paa certificates list
        async with http_session.get(
            f"{DCL_PRODUCTION_URL}/dcl/model/versions/{vid}/{pid}"
        ) as response:
            return await response.json()


async def _get_software_version(vid: int, pid: int, software_version: int) -> Any:
    """Check DCL if there are updates available for a particular node."""
    async with ClientSession(raise_for_status=True) as http_session:
        # fetch the paa certificates list
        async with http_session.get(
            f"{DCL_PRODUCTION_URL}/dcl/model/versions/{vid}/{pid}/{software_version}"
        ) as response:
            return await response.json()


async def _check_update_version(
    vid: int, pid: int, version: int, current_software_version: int
) -> None | dict:
    version_res: dict = await _get_software_version(vid, pid, version)
    if not isinstance(version_res, dict):
        raise TypeError("Unexpected DCL response.")

    if "modelVersion" not in version_res:
        raise ValueError("Unexpected DCL response.")

    version_candidate: dict = cast(dict, version_res["modelVersion"])

    # Check minApplicableSoftwareVersion/maxApplicableSoftwareVersion
    min_sw_version = version_candidate["minApplicableSoftwareVersion"]
    max_sw_version = version_candidate["maxApplicableSoftwareVersion"]
    if (
        current_software_version < min_sw_version
        or current_software_version > max_sw_version
    ):
        return None

    return version_candidate


async def check_for_update(
    vid: int,
    pid: int,
    current_software_version: int,
    requested_software_version: int | None = None,
) -> None | dict:
    """Check if there is a software update available on the DCL."""
    try:
        if requested_software_version is not None:
            return await _check_update_version(
                vid, pid, requested_software_version, current_software_version
            )

        # Get all versions and check each one of them.
        versions = await _get_software_versions(vid, pid)

        all_software_versions: list[int] = versions["modelVersions"]["softwareVersions"]
        newer_software_versions = [
            version
            for version in all_software_versions
            if version > current_software_version
        ]

        # Check if there is a newer software version available
        if not newer_software_versions:
            LOGGER.info("No newer software version available.")
            return None

        # Check if latest firmware is applicable, and backtrack from there
        for version in sorted(newer_software_versions, reverse=True):
            if version_candidate := await _check_update_version(
                vid, pid, version, current_software_version
            ):
                return version_candidate
            LOGGER.debug("Software version %d not applicable.", version)
        return None

    except (ClientError, TimeoutError) as err:
        LOGGER.error("Fetching software version failed: error %s", err, exc_info=err)
    return None
