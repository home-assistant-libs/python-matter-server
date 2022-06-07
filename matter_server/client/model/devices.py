from __future__ import annotations

from .device import MatterDevice

from matter_server.vendor.chip.clusters import Objects as all_clusters


class RootDevice(MatterDevice, device_type=0x0016):
    """Root device."""

    clusters = {
        all_clusters.Basic,
    }


class OnOffLight(MatterDevice, device_type=0x0100):
    """On/Off light."""

    clusters = {
        all_clusters.OnOff,
    }


class DimmableLight(MatterDevice, device_type=0x0101):
    """Dimmable light."""

    clusters = {all_clusters.OnOff, all_clusters.LevelControl}


class OnOffLightSwitch(MatterDevice, device_type=0x0103):
    """On/Off Light Switch."""


class OnOffPlugInUnit(MatterDevice, device_type=0x010A):
    """On/Off Plug-In Unit."""

    clusters = {
        all_clusters.OnOff,
    }


class DimmablePlugInUnit(MatterDevice, device_type=0x010B):
    """Dimmable Plug-In Unit."""

    clusters = {all_clusters.OnOff, all_clusters.LevelControl}
