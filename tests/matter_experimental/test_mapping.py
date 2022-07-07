"""Test that fixtures result in right data in Home Assistant."""
from __future__ import annotations

import json
import logging
from typing import TYPE_CHECKING

from homeassistant.helpers import device_registry as dr, entity_registry as er
import pytest

from custom_components.matter_experimental.const import DOMAIN
from custom_components.matter_experimental.device_platform import DEVICE_PLATFORM
from tests.matter_experimental.common import setup_integration_with_node_fixture

from ..fixtures import NODE_FIXTURES_ROOT, NODE_IN_HA_FIXTURES_ROOT


if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant


LOGGER = logging.getLogger(__name__)


@pytest.mark.parametrize(
    "node_fixture",
    [fix for fix in NODE_FIXTURES_ROOT.iterdir() if not fix.name.startswith("_")],
)
async def test_fixture(hass: HomeAssistant, hass_storage, node_fixture):
    node = await setup_integration_with_node_fixture(
        hass, hass_storage, node_fixture.name.rpartition(".")[0]
    )

    checks = json.loads((NODE_IN_HA_FIXTURES_ROOT / node_fixture.name).read_text())

    assert (node.bridge_device_type_instance is not None) == checks["is_bridge"]

    assert len(node.node_devices) == len(checks["node_devices"])

    dev_reg = dr.async_get(hass)
    ent_reg = er.async_get(hass)

    # Make sure all devices of this node are mapped in HA
    for md_idx, node_device in enumerate(node.node_devices):
        LOGGER.info("Checking device #%s %s", md_idx, node_device)
        nd_checks = checks["node_devices"][md_idx]

        device_entry = dev_reg.async_get_device(
            {(DOMAIN, node_device.device_info().uniqueID)}
        )

        node_entities = {
            ent.entity_id: ent
            for ent in er.async_entries_for_device(
                ent_reg, device_entry.id, include_disabled_entities=True
            )
        }

        for d_idx, instance in enumerate(node_device.device_type_instances()):
            LOGGER.info("Checking device type instance #%s %s", d_idx, instance)
            dti_checks = nd_checks["device_type_instances"][d_idx]
            assert instance.device_type.__name__ == dti_checks["type"]
            platforms = []

            for platform, devices in DEVICE_PLATFORM.items():
                entity_descriptions = devices.get(instance.device_type)

                if entity_descriptions is not None:
                    platforms.append(platform)

            assert platforms == dti_checks["platforms"]

            for entity_check in dti_checks["entities"]:
                assert entity_check["entity_id"] in node_entities
                node_entities.pop(entity_check["entity_id"])

                state = hass.states.get(entity_check["entity_id"])
                assert state is not None, entity_check["entity_id"]
                assert state.state == entity_check["state"]

                if "attributes" not in entity_check:
                    continue

                for attr, expected_value in entity_check["attributes"].items():
                    assert state.attributes.get(attr) == expected_value, attr

        assert (
            node_entities == {}
        ), f"Not all entities specified in check file: {', '.join(node_entities)}"
