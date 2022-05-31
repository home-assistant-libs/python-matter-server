"""Matter (experimental) integration."""
from __future__ import annotations

import asyncio

import voluptuous as vol
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EVENT_HOMEASSISTANT_STOP, Platform
from homeassistant.core import Event, HomeAssistant, ServiceCall, callback
from homeassistant.exceptions import ConfigEntryNotReady, HomeAssistantError
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.service import async_register_admin_service
from homeassistant.helpers.start import async_at_start

from matter_server.client.exceptions import CannotConnect, FailedCommand

from .adapter import MatterAdapter
from .const import DOMAIN
from .matter import Matter

PLATFORMS = [Platform.LIGHT]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Initialize set up entry."""
    matter = Matter(MatterAdapter(hass, entry))
    try:
        await matter.connect()
    except CannotConnect as err:
        raise ConfigEntryNotReady("Failed to connect to matter server") from err

    except Exception as err:
        matter.adapter.logger.exception("Failed to connect to matter server")
        raise ConfigEntryNotReady(
            "Unknown error connecting to the Matter server"
        ) from err

    matter.listen()
    await matter.driver_ready.wait()

    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = {}
        _async_init_services(hass)

    hass.data[DOMAIN][entry.entry_id] = matter

    hass.async_create_task(_finish_entry_setup(hass, entry, matter))

    return True


async def _finish_entry_setup(
    hass: HomeAssistant, entry: ConfigEntry, matter: Matter
) -> bool:
    await asyncio.gather(
        *[
            hass.config_entries.async_forward_entry_setup(entry, platform)
            for platform in PLATFORMS
        ]
    )
    tasks = [matter.adapter.setup_node(node) for node in matter.get_nodes()]
    if tasks:
        await asyncio.gather(*tasks)

    async def on_hass_stop(event: Event) -> None:
        """Handle incoming stop event from Home Assistant."""
        await matter.disconnect()

    entry.async_on_unload(
        hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STOP, on_hass_stop)
    )

    async def on_hass_start(event: Event) -> None:
        """Handle Home Assistant start."""
        await matter.finish_pending_work()

    async_at_start(hass, on_hass_start)

    return True


async def async_remove_config_entry_device(
    hass: HomeAssistant, config_entry: ConfigEntry, device_entry: dr.DeviceEntry
) -> bool:
    """Remove a config entry from a device."""
    unique_id = None

    for ident in device_entry.identifiers:
        if ident[0] == DOMAIN:
            unique_id = ident[1]
            break

    if not unique_id:
        return True

    matter: Matter = hass.data[DOMAIN][config_entry.entry_id]

    for node in matter.get_nodes():
        if node.unique_id == unique_id:
            await matter.delete_node(node.node_id)
            break

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_success = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_success:
        matter: Matter = hass.data[DOMAIN].pop(entry.entry_id)
        await matter.disconnect()

    return unload_success


@callback
def _async_init_services(hass: HomeAssistant) -> None:
    """Init services."""

    async def commission(call: ServiceCall) -> None:
        """Handle commissioning."""
        matter: Matter = list(hass.data[DOMAIN].values())[0]
        try:
            await matter.commission(call.data["code"])
        except FailedCommand as err:
            raise HomeAssistantError(str(err)) from err

    async_register_admin_service(
        hass,
        DOMAIN,
        "commission",
        commission,
        vol.Schema({"code": str}),
    )

    async def set_wifi(call: ServiceCall) -> None:
        """Handle set wifi creds."""
        matter: Matter = list(hass.data[DOMAIN].values())[0]
        try:
            await matter.client.driver.device_controller.SetWiFiCredentials(
                call.data["network_name"], call.data["password"]
            )
        except FailedCommand as err:
            raise HomeAssistantError(str(err)) from err

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

    async def set_thread(call: ServiceCall) -> None:
        """Handle set Thread creds."""
        matter: Matter = list(hass.data[DOMAIN].values())[0]
        thread_dataset = bytes.fromhex(call.data["thread_operation_dataset"])
        try:
            await matter.client.driver.device_controller.SetThreadOperationalDataset(
                thread_dataset
            )
        except FailedCommand as err:
            raise HomeAssistantError(str(err)) from err

    async_register_admin_service(
        hass,
        DOMAIN,
        "set_thread",
        set_thread,
        vol.Schema({"thread_operation_dataset": str}),
    )
