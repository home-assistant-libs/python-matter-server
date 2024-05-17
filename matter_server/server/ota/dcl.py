"""Handle OTA software version endpoints of the DCL."""

import logging
from typing import Any

from aiohttp import ClientError, ClientSession

from matter_server.server.helpers import DCL_PRODUCTION_URL

LOGGER = logging.getLogger(__name__)


async def get_software_versions(node_id: int, vid: int, pid: int) -> Any:
    """Check DCL if there are updates available for a particular node."""
    async with ClientSession(raise_for_status=True) as http_session:
        # fetch the paa certificates list
        async with http_session.get(
            f"{DCL_PRODUCTION_URL}/dcl/model/versions/{vid}/{pid}"
        ) as response:
            return await response.json()


async def get_software_version(
    node_id: int, vid: int, pid: int, software_version: int
) -> Any:
    """Check DCL if there are updates available for a particular node."""
    async with ClientSession(raise_for_status=True) as http_session:
        # fetch the paa certificates list
        async with http_session.get(
            f"{DCL_PRODUCTION_URL}/dcl/model/versions/{vid}/{pid}/{software_version}"
        ) as response:
            return await response.json()


async def check_updates(
    node_id: int, vid: int, pid: int, current_software_version: int
) -> None | dict:
    """Check if there is a newer software version available on the DCL."""
    try:
        versions = await get_software_versions(node_id, vid, pid)

        software_versions: list[int] = versions["modelVersions"]["softwareVersions"]
        latest_software_version = max(software_versions)
        if latest_software_version <= current_software_version:
            return None

        version: dict = await get_software_version(
            node_id, vid, pid, latest_software_version
        )
        if isinstance(version, dict) and "modelVersion" in version:
            result: Any = version["modelVersion"]
            if isinstance(result, dict):
                return result

        logging.error("Unexpected DCL response.")
        return None

    except (ClientError, TimeoutError) as err:
        LOGGER.error("Fetching software version failed: error %s", err, exc_info=err)
    return None
