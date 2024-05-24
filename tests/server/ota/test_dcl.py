"""Test DCL OTA updates."""

from unittest.mock import AsyncMock, patch

import pytest

from matter_server.server.ota.dcl import check_for_update

# Mock the DCL responses (sample from https://on.dcl.csa-iot.org/dcl/model/versions/4447/8194)
DCL_RESPONSE_SOFTWARE_VERSIONS = {
    "modelVersions": {
        "vid": 4447,
        "pid": 8194,
        "softwareVersions": [1000, 1011],
    }
}

# Mock the DCL responses (sample from https://on.dcl.csa-iot.org/dcl/model/versions/4447/8194/1011)
DCL_RESPONSE_SOFTWARE_VERSION_1011 = {
    "modelVersion": {
        "vid": 4447,
        "pid": 8194,
        "softwareVersion": 1011,
        "softwareVersionString": "1.0.1.1",
        "cdVersionNumber": 1,
        "firmwareInformation": "",
        "softwareVersionValid": True,
        "otaUrl": "https://cdn.aqara.com/cdn/opencloud-product/mainland/product-firmware/prd/aqara.matter.4447_8194/20240306154144_rel_up_to_enc_ota_sbl_app_aqara.matter.4447_8194_1.0.1.1_115F_2002_20240115195007_7a9b91.ota",
        "otaFileSize": "615708",
        "otaChecksum": "rFZ6WdH0DuuCf7HVoRmNjCF73mYZ98DGYpHoDKmf0Bw=",
        "otaChecksumType": 1,
        "minApplicableSoftwareVersion": 1000,
        "maxApplicableSoftwareVersion": 1010,
        "releaseNotesUrl": "",
        "creator": "cosmos1qpz3ghnqj6my7gzegkftzav9hpxymkx6zdk73v",
    }
}


@pytest.fixture(name="get_software_versions")
def mock_get_software_versions():
    """Mock the _get_software_versions function."""
    with patch(
        "matter_server.server.ota.dcl._get_software_versions",
        new_callable=AsyncMock,
        return_value=DCL_RESPONSE_SOFTWARE_VERSIONS,
    ) as mock:
        yield mock


@pytest.fixture(name="get_software_version")
def mock_get_software_version():
    """Mock the _get_software_version function."""
    with patch(
        "matter_server.server.ota.dcl._get_software_version",
        new_callable=AsyncMock,
        return_value=DCL_RESPONSE_SOFTWARE_VERSION_1011,
    ) as mock:
        yield mock


async def test_check_updates(get_software_versions, get_software_version):
    """Test the case where the latest software version is applicable."""
    # Call the function with a current software version of 1000
    result = await check_for_update(4447, 8194, 1000)

    assert result == DCL_RESPONSE_SOFTWARE_VERSION_1011["modelVersion"]


async def test_check_updates_not_applicable(
    get_software_versions, get_software_version
):
    """Test the case where the latest software version is not applicable."""
    # Call the function with a current software version of 1
    result = await check_for_update(4447, 8194, 1)

    assert result is None


async def test_check_updates_specific_version(get_software_version):
    """Test the case to get a specific version."""
    # Call the function with a current software version of 1000 and request 1011 as update
    result = await check_for_update(4447, 8194, 1000, 1011)

    assert result == DCL_RESPONSE_SOFTWARE_VERSION_1011["modelVersion"]
