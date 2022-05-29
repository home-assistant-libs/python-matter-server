"""Matter (experimental) integration."""
from __future__ import annotations
import asyncio

import voluptuous as vol
import logging

from homeassistant.const import CONF_URL, EVENT_HOMEASSISTANT_STOP, Platform
from homeassistant.core import Event, HomeAssistant, callback, ServiceCall
from homeassistant.config_entries import ConfigEntry
from homeassistant.exceptions import ConfigEntryNotReady, HomeAssistantError
from homeassistant.helpers import device_registry as dr, aiohttp_client
from homeassistant.helpers.service import async_register_admin_service

from matter_server.client.client import Client
from matter_server.client.exceptions import BaseMatterServerError, FailedCommand

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

    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = {}
        _async_init_services(hass)

    hass.data[DOMAIN][entry.entry_id] = {
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


@callback
def _async_init_services(hass: HomeAssistant) -> None:
    """Init services."""

    async def commission(call: ServiceCall) -> None:
        """Handle commissioning."""
        # Code written assuming single config entry.
        assert len(hass.data[DOMAIN]) == 1

        client: Client = list(hass.data[DOMAIN].values())[0]["client"]

        try:
            await client.driver.device_controller.CommissionWithCode(
                call.data["code"], call.data["node_id"]
            )
        except FailedCommand as err:
            raise HomeAssistantError(str(err)) from err

        # TODO notify that we now know a new device?

    async_register_admin_service(
        hass,
        DOMAIN,
        "commission",
        commission,
        vol.Schema(
            {
                "code": str,
                "node_id": int,
            }
        ),
    )

    async def set_wifi(call: ServiceCall) -> None:
        """Handle set wifi creds."""
        # Code written assuming single config entry.
        assert len(hass.data[DOMAIN]) == 1

        client: Client = list(hass.data[DOMAIN].values())[0]["client"]
        await client.driver.device_controller.SetWiFiCredentials(
            call.data["network_name"], call.data["password"]
        )

    async_register_admin_service(
        hass,
        DOMAIN,
        "set_wifi",
        set_wifi,
        vol.Schema(
            {
                "network_name": str,
                "password": str,
            }
        ),
    )
