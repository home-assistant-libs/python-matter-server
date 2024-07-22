"""Test DCL OTA updates."""

import json
import pathlib
from typing import Any
from unittest.mock import MagicMock

from aioresponses import aioresponses
import pytest

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


@pytest.fixture(name="get_software_versions", autouse=True)
def _mock_get_software_versions(aioresponse) -> None:
    """Mock the _get_software_versions function."""
    data = _load_fixture("4447-8194.json")
    aioresponse.get(url="/dcl/model/versions/4447/8194", status=200, payload=data)
    aioresponse.get(
        url="/dcl/model/versions/4447/8194/1000",
        payload=_load_fixture("4447-8194-1000.json"),
    )


async def test_check_updates(aioresponse):
    """Test the case where the latest software version is applicable."""
    # Call the function with a current software version of 1000
    data = _load_fixture("4447-8194-1011-valid.json")
    aioresponse.get(url="/dcl/model/versions/4447/8194/1011", status=200, payload=data)
    result = await check_for_update(MagicMock(), 4447, 8194, 1000)

    assert result == data["modelVersion"]


async def test_check_updates_not_applicable(aioresponse):
    """Test the case where the latest software version is not applicable."""
    # Call the function with a current software version of 2000
    data = _load_fixture("4447-8194-1011-valid.json")
    aioresponse.get(url="/dcl/model/versions/4447/8194/1011", status=200, payload=data)
    result = await check_for_update(MagicMock(), 4447, 8194, 2000)

    assert result is None


async def test_check_updates_not_applicable_not_valid(aioresponse):
    """Test the case where the latest software version is not valid."""
    data = _load_fixture("4447-8194-1011-invalid.json")
    aioresponse.get(url="/dcl/model/versions/4447/8194/1011", status=200, payload=data)
    result = await check_for_update(MagicMock(), 4447, 8194, 1000)

    assert result is None


async def test_check_updates_specific_version(aioresponse):
    """Test the case to get a specific version."""
    # Call the function with a current software version of 1000 and request 1011 as update
    data = _load_fixture("4447-8194-1011-valid.json")
    aioresponse.get(url="/dcl/model/versions/4447/8194/1011", payload=data)
    result = await check_for_update(MagicMock(), 4447, 8194, 1000, 1011)

    assert result == data["modelVersion"]


async def test_check_no_update_if_url_empty(aioresponse):
    """Test the case checks if latest version gets picked version."""
    # Call the function with a current software version of 1000 and request 1011 as update
    data = _load_fixture("4442-67.json")
    aioresponse.get(url="/dcl/model/versions/4442/67", payload=data)
    data = _load_fixture("4442-67-197888.json")
    aioresponse.get(url="/dcl/model/versions/4442/67/197888", payload=data)
    data = _load_fixture("4442-67-197910.json")
    aioresponse.get(url="/dcl/model/versions/4442/67/197910", payload=data)
    data = _load_fixture("4442-67-198340.json")
    aioresponse.get(url="/dcl/model/versions/4442/67/198340", payload=data)
    result = await check_for_update(MagicMock(), 4442, 67, 197120)

    assert result is None
