"""Matter to HA adapter."""
import logging
from abc import abstractmethod

import aiohttp
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_URL
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .node import MatterNode
from .storage import MatterStorage


class AbstractMatterAdapter:

    logger: logging.Logger

    @abstractmethod
    def get_server_url(self) -> str:
        """Return server URL."""

    @abstractmethod
    def get_client_session(self) -> aiohttp.ClientSession:
        """Return aiohttp client session."""

    @abstractmethod
    def get_storage(self) -> MatterStorage:
        """Return storage."""

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
        self.storage = MatterStorage(self.hass)

    def get_server_url(self) -> str:
        return self.config_entry.data[CONF_URL]

    def get_client_session(self) -> aiohttp.ClientSession:
        return async_get_clientsession(self.hass)

    def get_storage(self) -> MatterStorage:
        return self.storage

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
