from __future__ import annotations

from functools import lru_cache
import logging
import json
import asyncio
from typing import TYPE_CHECKING
from unittest.mock import Mock, patch

from matter_server.client.client import Client
from matter_server.client.model.driver import Driver
from tests.fixtures import NODE_FIXTURES_ROOT
from pytest_homeassistant_custom_component.common import MockConfigEntry
from matter_server.client.model.node import MatterNode

from matter_server.common import json_utils
from matter_server.vendor.chip.clusters.ObjectsVersion import CLUSTER_OBJECT_VERSION

from tests.test_utils.mock_matter import get_mock_matter

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant


MOCK_COMPR_FABRIC_ID = 1234
LOGGER = logging.getLogger(__name__)


class MockClient(Client):

    mock_client_disconnect: asyncio.Event

    async def connect(self):
        self.server_info = Mock(compressedFabricId=MOCK_COMPR_FABRIC_ID)

    async def listen(self, driver_ready):
        self.driver = Driver(self)
        driver_ready.set()
        self.mock_client_disconnect = asyncio.Event()
        await self.mock_client_disconnect.wait()


@lru_cache(maxsize=None)
def load_node_fixture(fixture: str) -> str:
    """Load a fixture."""
    return (NODE_FIXTURES_ROOT / f"{fixture}.json").read_text()


def load_and_parse_node_fixture(fixture: str):
    return json.loads(load_node_fixture(fixture), cls=json_utils.CHIPJSONDecoder)


async def setup_integration_with_node_fixture(
    hass: HomeAssistant, hass_storage, node_fixture: str
) -> MatterNode:
    """Set up Matter integration with fixture as node."""
    node_data = load_and_parse_node_fixture(node_fixture)
    node = MatterNode(
        get_mock_matter(),
        node_data,
    )
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

    return node
