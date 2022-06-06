"""Matter (experimental) integration."""
from __future__ import annotations

import asyncio
from pathlib import Path

import async_timeout
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EVENT_HOMEASSISTANT_STOP
from homeassistant.core import Event, HomeAssistant, ServiceCall, callback
from homeassistant.exceptions import ConfigEntryNotReady, HomeAssistantError
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.service import async_register_admin_service
import voluptuous as vol

from matter_server.client.exceptions import CannotConnect, FailedCommand
from matter_server.client.matter import Matter

from .adapter import MatterAdapter, get_matter_store
from .const import DOMAIN
from .device_platform import DEVICE_PLATFORM


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

    async def on_hass_stop(event: Event) -> None:
        """Handle incoming stop event from Home Assistant."""
        await matter.disconnect()

    entry.async_on_unload(
        hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STOP, on_hass_stop)
    )

    matter.listen()
    try:
        async with async_timeout.timeout(30):
            await matter.driver_ready.wait()
    except asyncio.TimeoutError as err:
        raise ConfigEntryNotReady("Matter driver not ready") from err

    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = {}
        _async_init_services(hass)

    hass.data[DOMAIN][entry.entry_id] = matter

    hass.config_entries.async_setup_platforms(entry, DEVICE_PLATFORM)

    return True


async def async_remove_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Config entry is being removed."""
    # Remove storage file.
    storage_path = get_matter_store(hass, entry).path
    await hass.async_add_executor_job(Path(storage_path).unlink)


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
    unload_success = await hass.config_entries.async_unload_platforms(
        entry, DEVICE_PLATFORM
    )

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
            await matter.client.driver.device_controller.set_wifi_credentials(
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
            await matter.client.driver.device_controller.set_thread_operational_dataset(
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

    async def open_commissioning_window(call: ServiceCall) -> None:
        """Open commissioning window on specific node."""
        matter: Matter = list(hass.data[DOMAIN].values())[0]
        try:
            await matter.client.driver.device_controller.open_commissioning_window(
                call.data["node_id"]
            )
        except FailedCommand as err:
            raise HomeAssistantError(str(err)) from err

    async_register_admin_service(
        hass,
        DOMAIN,
        "open_commissioning_window",
        open_commissioning_window,
        vol.Schema({"node_id": int}),
    )
