"""Matter to HA adapter."""
from __future__ import annotations

import logging
from abc import abstractmethod
from typing import TYPE_CHECKING, Callable

import aiohttp
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_URL, Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.storage import Store
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers import device_registry as dr

from matter_server.client.adapter import AbstractMatterAdapter

from .const import DOMAIN
from .device_platform import DEVICE_PLATFORM

if TYPE_CHECKING:
    from matter_server.client.model.node import MatterNode

STORAGE_MAJOR_VERSION = 1
STORAGE_MINOR_VERSION = 0


class MatterAdapter(AbstractMatterAdapter):
    def __init__(self, hass: HomeAssistant, config_entry: ConfigEntry) -> None:
        self.hass = hass
        self.config_entry = config_entry
        self.logger = logging.getLogger(__name__)
        self._store = Store(
            hass,
            STORAGE_MAJOR_VERSION,
            DOMAIN,
            minor_version=STORAGE_MINOR_VERSION,
        )
        self.platform_handlers: dict[Platform, AddEntitiesCallback] = {}

    def register_platform_handler(
        self, platform: Platform, add_entities: AddEntitiesCallback
    ) -> None:
        self.platform_handlers[platform] = add_entities

    @abstractmethod
    async def load_data(self) -> dict | None:
        """Load data."""
        return await self._store.async_load()

    @abstractmethod
    async def save_data(self, data: dict) -> None:
        """Save data."""
        await self._store.async_save(data)

    @abstractmethod
    def delay_save_data(self, get_data: Callable[[], dict]) -> None:
        """Save data, but not right now."""
        self._store.async_delay_save(get_data, 60)

    def get_server_url(self) -> str:
        return self.config_entry.data[CONF_URL]

    def get_client_session(self) -> aiohttp.ClientSession:
        return async_get_clientsession(self.hass)

    async def setup_node(self, node: MatterNode) -> None:
        """Set up an node."""
        self.logger.debug("Setting up entities for node %s", node.node_id)

        basic_info = node.root_device.basic_info

        kwargs = {}
        if basic_info["nodeLabel"]:
            kwargs["name"] = basic_info["nodeLabel"]
        if basic_info["location"]:
            kwargs["suggested_area"] = basic_info["location"]

        dr.async_get(self.hass).async_get_or_create(
            config_entry_id=self.config_entry.entry_id,
            identifiers={(DOMAIN, basic_info["uniqueID"])},
            hw_version=basic_info["hardwareVersionString"],
            sw_version=basic_info["softwareVersionString"],
            manufacturer=basic_info["vendorName"],
            model=basic_info["productName"],
            **kwargs,
        )

        for device in node.devices:
            created = False
            device_type = type(device)

            for platform, devices in DEVICE_PLATFORM.items():
                device_mappings = devices.get(device_type)

                if device_mappings is None:
                    continue

                self.logger.debug(
                    "Creating %s entity for %s (%s)",
                    platform,
                    type(device),
                    device.device_type,
                )

                if not isinstance(device_mappings, list):
                    device_mappings = [device_mappings]

                self.platform_handlers[platform](
                    [
                        device_mapping.entity_cls(device, device_mapping)
                        for device_mapping in device_mappings
                    ]
                )
                created = True

            if not created:
                self.logger.warning(
                    "Found unsupported device %s (%s)",
                    type(device).__name__,
                    device.device_type,
                )

    async def handle_server_disconnected(self, should_reload: bool) -> None:
        # The entry needs to be reloaded since a new driver state
        # will be acquired on reconnect.
        # All model instances will be replaced when the new state is acquired.
        if should_reload and self.hass.is_running:
            self.logger.info("Disconnected from server. Reloading")
            self.hass.async_create_task(
                self.hass.config_entries.async_reload(self.config_entry.entry_id)
            )
