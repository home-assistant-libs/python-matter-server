"""Matter (experimental) integration."""
from __future__ import annotations
import asyncio

import logging

from homeassistant.const import CONF_URL, EVENT_HOMEASSISTANT_STOP, Platform
from homeassistant.core import Event, HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers import device_registry as dr, aiohttp_client

from matter_server.client.client import Client
from matter_server.client.exceptions import BaseMatterServerError

from .const import DOMAIN

PLATFORMS = [Platform.LIGHT]
_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Initialize set up entry."""
    client = Client(entry.data[CONF_URL], aiohttp_client.async_get_clientsession(hass))
    try:
        await client.connect()
    except Exception as err:
        _LOGGER.exception("Error to initialize Matter")
        raise ConfigEntryNotReady from err

    driver_ready = asyncio.Event()

    listen_task = asyncio.create_task(_client_listen(hass, entry, client, driver_ready))

    await driver_ready.wait()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = {
        "client": client,
        "listen_task": listen_task,
    }

    hass.config_entries.async_setup_platforms(entry, PLATFORMS)

    async def on_hass_stop(event: Event) -> None:
        """Handle incoming stop event from Home Assistant."""
        listen_task.cancel()
        await listen_task

    entry.async_on_unload(
        hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STOP, on_hass_stop)
    )

    return True


async def async_remove_config_entry_device(
    hass: HomeAssistant, config_entry: ConfigEntry, device_entry: dr.DeviceEntry
) -> bool:
    """Remove a config entry from a device."""
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_success = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_success:
        listen_task = hass.data[DOMAIN].pop(entry.entry_id)["listen_task"]
        listen_task.cancel()
        await listen_task

    return unload_success


async def _client_listen(
    hass: HomeAssistant,
    entry: ConfigEntry,
    client: Client,
    driver_ready: asyncio.Event,
) -> None:
    """Listen with the client."""
    should_reload = True
    try:
        await client.listen(driver_ready)
    except asyncio.CancelledError:
        should_reload = False
    except BaseMatterServerError as err:
        _LOGGER.error("Failed to listen: %s", err)
    except Exception as err:  # pylint: disable=broad-except
        # We need to guard against unknown exceptions to not crash this task.
        _LOGGER.exception("Unexpected exception: %s", err)

    # The entry needs to be reloaded since a new driver state
    # will be acquired on reconnect.
    # All model instances will be replaced when the new state is acquired.
    if should_reload:
        _LOGGER.info("Disconnected from server. Reloading integration")
        hass.async_create_task(hass.config_entries.async_reload(entry.entry_id))
