"""Matter to HA adapter."""
from __future__ import annotations
import logging
from abc import abstractmethod
from typing import Callable

import aiohttp
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_URL
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.storage import Store

from .const import DOMAIN
from .node import MatterNode

STORAGE_MAJOR_VERSION = 1
STORAGE_MINOR_VERSION = 0


class AbstractMatterAdapter:

    logger: logging.Logger

    @abstractmethod
    async def load_data(self) -> dict | None:
        """Load data."""

    @abstractmethod
    async def save_data(self, data: dict) -> None:
        """Save data."""

    @abstractmethod
    def delay_save_data(self, get_data: Callable[[], dict]) -> None:
        """Save data, but not right now."""

    @abstractmethod
    def get_server_url(self) -> str:
        """Return server URL."""

    @abstractmethod
    def get_client_session(self) -> aiohttp.ClientSession:
        """Return aiohttp client session."""

    @abstractmethod
    async def setup_node(self, node: MatterNode) -> None:
        """Set up an node."""

    @abstractmethod
    async def handle_server_disconnected(self, should_reload: bool) -> None:
        """Server disconnected."""


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
        self.logger.info("Setting up entities for node %s", node.node_id)

    async def handle_server_disconnected(self, should_reload: bool) -> None:
        # The entry needs to be reloaded since a new driver state
        # will be acquired on reconnect.
        # All model instances will be replaced when the new state is acquired.
        if should_reload:
            self.logger.info("Disconnected from server. Reloading")
            self.hass.async_create_task(
                self.hass.config_entries.async_reload(self.config_entry.entry_id)
            )
