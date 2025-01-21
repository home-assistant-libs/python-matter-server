"""Test DCL OTA updates."""

import json
import pathlib
from typing import Any
from unittest.mock import MagicMock

from aioresponses import aioresponses
import pytest

from matter_server.server.helpers import DCL_PRODUCTION_URL
from matter_server.server.ota.dcl import check_for_update


def _load_fixture(file_name) -> Any:
    path = pathlib.Path(__file__).parent.joinpath("fixtures", file_name)
    with open(path, "r") as f:
        return json.load(f)


@pytest.fixture(name="aioresponse")
def mock_aioresponse():
    """Mock the aiohttp.ClientSession."""
    with aioresponses() as m:
        yield m


def mock_dcl_version(
    aioresponse, vid: int, pid: int, version: int | None = None, suffix: str = ""
) -> dict:
    """Test."""
    if version:
        data = _load_fixture(f"{vid}-{pid}-{version}{suffix}.json")
        url = DCL_PRODUCTION_URL + f"/dcl/model/versions/{vid}/{pid}/{version}"
    else:
        data = _load_fixture(f"{vid}-{pid}{suffix}.json")
        url = DCL_PRODUCTION_URL + f"/dcl/model/versions/{vid}/{pid}"
    aioresponse.get(url=url, status=200, payload=data)
    return data


@pytest.fixture(name="get_software_versions", autouse=True)
def _mock_get_software_versions(aioresponse) -> None:
    """Mock the _get_software_versions function."""
    mock_dcl_version(aioresponse, 4447, 8194)
    mock_dcl_version(aioresponse, 4447, 8194, 1000)


async def test_check_updates(aioresponse):
    """Test the case where the latest software version is applicable."""
    # Call the function with a current software version of 1000
    data = mock_dcl_version(aioresponse, 4447, 8194, 1011, "-valid")
    result = await check_for_update(MagicMock(), 4447, 8194, 1000)

    assert result == data["modelVersion"]


async def test_check_updates_not_applicable(aioresponse):
    """Test the case where the latest software version is not applicable."""
    # Call the function with a current software version of 2000
    mock_dcl_version(aioresponse, 4447, 8194, 1011, "-valid")
    result = await check_for_update(MagicMock(), 4447, 8194, 2000)

    assert result is None


async def test_check_updates_not_applicable_not_valid(aioresponse):
    """Test the case where the latest software version is not valid."""
    mock_dcl_version(aioresponse, 4447, 8194, 1011, "-invalid")
    result = await check_for_update(MagicMock(), 4447, 8194, 1000)

    assert result is None


async def test_check_updates_specific_version(aioresponse):
    """Test the case to get a specific version."""
    # Call the function with a current software version of 1000 and request 1011 as update
    data = mock_dcl_version(aioresponse, 4447, 8194, 1011, "-valid")
    result = await check_for_update(MagicMock(), 4447, 8194, 1000, 1011)

    assert result == data["modelVersion"]


async def test_check_no_update_if_url_empty(aioresponse):
    """Test the case checks if latest version gets picked version."""
    # Call the function with a current software version of 1000 and request 1011 as update
    mock_dcl_version(aioresponse, 4442, 67)
    mock_dcl_version(aioresponse, 4442, 67, 197888)
    mock_dcl_version(aioresponse, 4442, 67, 197910)
    mock_dcl_version(aioresponse, 4442, 67, 198340)
    result = await check_for_update(MagicMock(), 4442, 67, 197120)

    assert result is None
