"""Test that fixtures result in right data in Home Assistant."""
import json

import pytest

from custom_components.matter_experimental.device_platform import DEVICE_PLATFORM
from matter_server.client.model.node import MatterNode
from matter_server.common import json_utils

from ..fixtures import NODE_FIXTURES_ROOT, NODE_IN_HA_FIXTURES_ROOT

from tests.test_utils.mock_matter import get_mock_matter


@pytest.mark.parametrize("node_fixture", NODE_FIXTURES_ROOT.iterdir())
def test_fixture(node_fixture):
    node = MatterNode(
        get_mock_matter(),
        json.loads(node_fixture.read_text(), cls=json_utils.CHIPJSONDecoder),
    )
    checks = json.loads((NODE_IN_HA_FIXTURES_ROOT / node_fixture.name).read_text())

    assert (node.bridge_device_type_instance is not None) == checks["is_bridge"]

    assert len(node.node_devices) == len(checks["node_devices"])

    # Make sure all devices of this node are mapped in HA
    for md_idx, node_device in enumerate(node.node_devices):
        nd_checks = checks["node_devices"][md_idx]

        info = node_device.device_info()
        for key in "vendorName", "productName", "uniqueID":
            assert getattr(info, key) == nd_checks[key], key

        for d_idx, device in enumerate(node_device.device_type_instances()):
            dti_checks = nd_checks["device_type_instances"][d_idx]
            assert device.device_type.__name__ == dti_checks["type"]
            platforms = []

            for platform, devices in DEVICE_PLATFORM.items():
                device_mappings = devices.get(device.device_type)

                if device_mappings is not None:
                    platforms.append(platform)

            assert platforms == dti_checks["platforms"]
