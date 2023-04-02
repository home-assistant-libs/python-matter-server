"""
Util to resolve the vendor name from the CSA Vendor ID.
"""

import logging

from aiohttp import ClientError, ClientSession

LOGGER = logging.getLogger(__name__)
PRODUCTION_URL = "https://on.dcl.csa-iot.org"

VENDORS: dict[int, str] = {}


async def fetch_vendors() -> None:
    """Fetch the vendor names from the CSA."""
    LOGGER.info("Fetching the latest vendor info from DCL.")
    vendors: dict[int, str] = {}
    try:
        async with ClientSession(raise_for_status=True) as session:
            async with session.get(
                f"{PRODUCTION_URL}/dcl/vendorinfo/vendors"
            ) as response:
                data = await response.json()
                for vendorinfo in data["vendorInfo"]:
                    vendors[vendorinfo["vendorID"]] = vendorinfo["vendorName"]
    except ClientError as err:
        LOGGER.error("Unable to fetch vendor info from DCL: %s", err)
    else:
        LOGGER.info("Fetched %s vendor names from DCL.", len(vendors))

    VENDORS.update(vendors)
