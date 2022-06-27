"""Test that fixtures result in right data in Home Assistant."""
from __future__ import annotations
import asyncio

import json
from typing import TYPE_CHECKING
from unittest.mock import Mock, patch

import pytest

from custom_components.matter_experimental.device_platform import DEVICE_PLATFORM
from matter_server.client.client import Client
from matter_server.client.model.driver import Driver
from matter_server.client.model.node import MatterNode
from matter_server.common import json_utils
from pytest_homeassistant_custom_component.common import MockConfigEntry

from matter_server.vendor.chip.clusters.ObjectsVersion import CLUSTER_OBJECT_VERSION

from ..fixtures import NODE_FIXTURES_ROOT, NODE_IN_HA_FIXTURES_ROOT

from tests.test_utils.mock_matter import get_mock_matter

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant


MOCK_COMPR_FABRIC_ID = 1234


class MockClient(Client):

    mock_client_disconnect: asyncio.Event

    async def connect(self):
        self.server_info = Mock(compressedFabricId=MOCK_COMPR_FABRIC_ID)

    async def listen(self, driver_ready):
        self.driver = Driver(self)
        driver_ready.set()
        self.mock_client_disconnect = asyncio.Event()
        await self.mock_client_disconnect.wait()

    # async def async_send_command(
    #     self,
    #     command: str,
    #     args: dict[str, Any],
    #     require_schema: int | None = None,
    # ):
    #     if command == "device_controller.Read":
    #         if args.get("reportInterval"):
    #             return {"subscription_id": 1}
    #         return {}


@pytest.mark.parametrize("node_fixture", NODE_FIXTURES_ROOT.iterdir())
async def test_fixture(hass: HomeAssistant, hass_storage, node_fixture):
    node_data = json.loads(node_fixture.read_text(), cls=json_utils.CHIPJSONDecoder)
    node = MatterNode(
        get_mock_matter(),
        node_data,
    )
    checks = json.loads((NODE_IN_HA_FIXTURES_ROOT / node_fixture.name).read_text())

    assert (node.bridge_device_type_instance is not None) == checks["is_bridge"]

    assert len(node.node_devices) == len(checks["node_devices"])

    entities_to_check = []

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

            entities_to_check.extend(dti_checks["entities"])

    # Set up HA
    config_entry = MockConfigEntry(
        domain="matter_experimental", data={"url": "http://mock-matter-server-url"}
    )
    config_entry.add_to_hass(hass)

    storage_key = f"matter_experimental_{config_entry.entry_id}"
    hass_storage[storage_key] = {
        "version": 1,
        "minor_version": 0,
        "key": storage_key,
        "data": {
            "compressed_fabric_id": MOCK_COMPR_FABRIC_ID,
            "next_node_id": 4339,
            "node_interview_version": CLUSTER_OBJECT_VERSION,
            "nodes": {str(node.node_id): node_data},
        },
    }

    async def mock_init_matter_device(self):
        self._update_from_device()

    with patch("matter_server.client.matter.Client", MockClient), patch(
        "custom_components.matter_experimental.entity.MatterEntity.init_matter_device",
        mock_init_matter_device,
    ):
        assert await hass.config_entries.async_setup(config_entry.entry_id)
        await hass.async_block_till_done()

    for entity_check in entities_to_check:
        state = hass.states.get(entity_check["entity_id"])
        assert state is not None, entity_check["entity_id"]
        assert state.state == entity_check["state"]

        if "attributes" not in entity_check:
            continue

        for attr, expected_value in entity_check["attributes"].items():
            assert state.attributes.get(attr) == expected_value, attr
