"""
Definitions for all known Device types.

This file is auto generated from `zcl/data-model/chip/matter-devices.xml`
Do not override!
"""
from __future__ import annotations

import typing

from chip.clusters import Objects as all_clusters

ALL_TYPES: dict[int, type["DeviceType"]] = {}


class DeviceType:
    """Base class for Matter device types."""

    device_type: int
    clusters: set[type[all_clusters.Cluster]]

    def __init_subclass__(cls, *, device_type: int, **kwargs: typing.Any) -> None:
        """Register a subclass."""
        super().__init_subclass__(**kwargs)
        cls.device_type = device_type
        ALL_TYPES[device_type] = cls

    def __hash__(self) -> int:
        """Return unique hash for this object."""
        return self.device_type


class OrphanClusters(DeviceType, device_type=0xF001):
    """Orphan Clusters."""

    clusters = {
        all_clusters.ProxyConfiguration,
        all_clusters.ProxyDiscovery,
        all_clusters.ProxyValid,
        all_clusters.PulseWidthModulation,
    }


class RootNode(DeviceType, device_type=0x0016):
    """Root Node."""

    clusters = {
        all_clusters.AccessControl,
        all_clusters.BasicInformation,
        all_clusters.Descriptor,
        all_clusters.GeneralCommissioning,
        all_clusters.PowerSourceConfiguration,
        all_clusters.TimeSynchronization,
        all_clusters.GroupKeyManagement,
        all_clusters.NetworkCommissioning,
        all_clusters.AdministratorCommissioning,
        all_clusters.OperationalCredentials,
        all_clusters.LocalizationConfiguration,
        all_clusters.TimeFormatLocalization,
        all_clusters.UnitLocalization,
        all_clusters.GeneralDiagnostics,
        all_clusters.DiagnosticLogs,
        all_clusters.SoftwareDiagnostics,
        all_clusters.EthernetNetworkDiagnostics,
        all_clusters.WiFiNetworkDiagnostics,
        all_clusters.ThreadNetworkDiagnostics,
    }


class PowerSource(DeviceType, device_type=0x0011):
    """Power Source."""

    clusters = {
        all_clusters.Descriptor,
        all_clusters.PowerSource,
    }


class OtaRequestor(DeviceType, device_type=0x0012):
    """OTA Requestor."""

    clusters = {
        all_clusters.Descriptor,
        all_clusters.OtaSoftwareUpdateRequestor,
    }


class OtaProvider(DeviceType, device_type=0x0014):
    """OTA Provider."""

    clusters = {
        all_clusters.Descriptor,
        all_clusters.OtaSoftwareUpdateProvider,
    }


class Aggregator(DeviceType, device_type=0x000E):
    """Aggregator."""

    clusters = {
        all_clusters.Descriptor,
        all_clusters.Actions,
    }


class BridgedDevice(DeviceType, device_type=0x0013):
    """Bridged Device."""

    clusters = {
        all_clusters.Descriptor,
        all_clusters.BridgedDeviceBasicInformation,
        all_clusters.PowerSourceConfiguration,
        all_clusters.PowerSource,
    }


class OnOffLight(DeviceType, device_type=0x0100):
    """On/Off Light."""

    clusters = {
        all_clusters.Identify,
        all_clusters.Descriptor,
        all_clusters.Groups,
        all_clusters.Scenes,
        all_clusters.OnOff,
        all_clusters.LevelControl,
    }


class DimmableLight(DeviceType, device_type=0x0101):
    """Dimmable Light."""

    clusters = {
        all_clusters.Identify,
        all_clusters.Descriptor,
        all_clusters.Binding,
        all_clusters.Groups,
        all_clusters.Scenes,
        all_clusters.OnOff,
        all_clusters.LevelControl,
    }


class ColorTemperatureLight(DeviceType, device_type=0x010C):
    """Color Temperature Light."""

    clusters = {
        all_clusters.Identify,
        all_clusters.Descriptor,
        all_clusters.Groups,
        all_clusters.Scenes,
        all_clusters.OnOff,
        all_clusters.LevelControl,
        all_clusters.ColorControl,
    }


class ExtendedColorLight(DeviceType, device_type=0x010D):
    """Extended Color Light."""

    clusters = {
        all_clusters.Identify,
        all_clusters.Descriptor,
        all_clusters.Groups,
        all_clusters.Scenes,
        all_clusters.OnOff,
        all_clusters.LevelControl,
        all_clusters.ColorControl,
    }


class OnOffPlugInUnit(DeviceType, device_type=0x010A):
    """On/Off Plug-in Unit."""

    clusters = {
        all_clusters.Identify,
        all_clusters.Descriptor,
        all_clusters.Groups,
        all_clusters.Scenes,
        all_clusters.OnOff,
        all_clusters.LevelControl,
    }


class DimmablePlugInUnit(DeviceType, device_type=0x010B):
    """Dimmable Plug-in Unit."""

    clusters = {
        all_clusters.Identify,
        all_clusters.Descriptor,
        all_clusters.Groups,
        all_clusters.Scenes,
        all_clusters.OnOff,
        all_clusters.LevelControl,
    }


class Pump(DeviceType, device_type=0x0303):
    """Pump."""

    clusters = {
        all_clusters.Identify,
        all_clusters.Descriptor,
        all_clusters.Binding,
        all_clusters.Groups,
        all_clusters.Scenes,
        all_clusters.OnOff,
        all_clusters.PumpConfigurationAndControl,
        all_clusters.LevelControl,
        all_clusters.TemperatureMeasurement,
        all_clusters.PressureMeasurement,
        all_clusters.FlowMeasurement,
    }


class OnOffLightSwitch(DeviceType, device_type=0x0103):
    """On/Off Light Switch."""

    clusters = {
        all_clusters.Identify,
        all_clusters.Descriptor,
        all_clusters.Binding,
    }


class DimmerSwitch(DeviceType, device_type=0x0104):
    """Dimmer Switch."""

    clusters = {
        all_clusters.Identify,
        all_clusters.Descriptor,
        all_clusters.Binding,
    }


class ColorDimmerSwitch(DeviceType, device_type=0x0105):
    """Color Dimmer Switch."""

    clusters = {
        all_clusters.Identify,
        all_clusters.Descriptor,
        all_clusters.Binding,
    }


class ControlBridge(DeviceType, device_type=0x0840):
    """Control Bridge."""

    clusters = {
        all_clusters.Identify,
        all_clusters.Descriptor,
        all_clusters.Binding,
    }


class PumpController(DeviceType, device_type=0x0304):
    """Pump Controller."""

    clusters = {
        all_clusters.Identify,
        all_clusters.Descriptor,
        all_clusters.Binding,
    }


class GenericSwitch(DeviceType, device_type=0x000F):
    """Generic Switch."""

    clusters = {
        all_clusters.Identify,
        all_clusters.Descriptor,
        all_clusters.Switch,
        all_clusters.FixedLabel,
        all_clusters.UserLabel,
    }


class ContactSensor(DeviceType, device_type=0x0015):
    """Contact Sensor."""

    clusters = {
        all_clusters.Identify,
        all_clusters.Descriptor,
        all_clusters.BooleanState,
    }


class LightSensor(DeviceType, device_type=0x0106):
    """Light Sensor."""

    clusters = {
        all_clusters.Identify,
        all_clusters.Descriptor,
        all_clusters.Binding,
        all_clusters.IlluminanceMeasurement,
    }


class OccupancySensor(DeviceType, device_type=0x0107):
    """Occupancy Sensor."""

    clusters = {
        all_clusters.Identify,
        all_clusters.Descriptor,
        all_clusters.Binding,
        all_clusters.OccupancySensing,
    }


class TemperatureSensor(DeviceType, device_type=0x0302):
    """Temperature Sensor."""

    clusters = {
        all_clusters.Identify,
        all_clusters.Descriptor,
        all_clusters.TemperatureMeasurement,
    }


class PressureSensor(DeviceType, device_type=0x0305):
    """Pressure Sensor."""

    clusters = {
        all_clusters.Identify,
        all_clusters.Descriptor,
        all_clusters.PressureMeasurement,
    }


class FlowSensor(DeviceType, device_type=0x0306):
    """Flow Sensor."""

    clusters = {
        all_clusters.Identify,
        all_clusters.Descriptor,
        all_clusters.FlowMeasurement,
    }


class HumiditySensor(DeviceType, device_type=0x0307):
    """Humidity Sensor."""

    clusters = {
        all_clusters.Identify,
        all_clusters.Descriptor,
        all_clusters.RelativeHumidityMeasurement,
    }


class OnOffSensor(DeviceType, device_type=0x0850):
    """On/Off Sensor."""

    clusters = {
        all_clusters.Identify,
        all_clusters.Descriptor,
        all_clusters.Binding,
    }


class DoorLock(DeviceType, device_type=0x000A):
    """Door Lock."""

    clusters = {
        all_clusters.Identify,
        all_clusters.Descriptor,
        all_clusters.Binding,
        all_clusters.DoorLock,
    }


class DoorLockController(DeviceType, device_type=0x000B):
    """Door Lock Controller."""

    clusters = {
        all_clusters.Descriptor,
        all_clusters.Binding,
        all_clusters.TimeSynchronization,
    }


class WindowCovering(DeviceType, device_type=0x0202):
    """Window Covering."""

    clusters = {
        all_clusters.Identify,
        all_clusters.Descriptor,
        all_clusters.Scenes,
        all_clusters.Groups,
        all_clusters.WindowCovering,
    }


class WindowCoveringController(DeviceType, device_type=0x0203):
    """Window Covering Controller."""

    clusters = {
        all_clusters.Identify,
        all_clusters.Descriptor,
        all_clusters.Binding,
    }


class HeatingCoolingUnit(DeviceType, device_type=0x0300):
    """Heating/Cooling Unit."""

    clusters = {
        all_clusters.Identify,
        all_clusters.Descriptor,
        all_clusters.Binding,
        all_clusters.Groups,
        all_clusters.Scenes,
        all_clusters.FanControl,
        all_clusters.LevelControl,
        all_clusters.OnOff,
    }


class Thermostat(DeviceType, device_type=0x0301):
    """Thermostat."""

    clusters = {
        all_clusters.Identify,
        all_clusters.Descriptor,
        all_clusters.Binding,
        all_clusters.Scenes,
        all_clusters.Groups,
        all_clusters.Thermostat,
        all_clusters.TimeSynchronization,
        all_clusters.ThermostatUserInterfaceConfiguration,
    }


class Fan(DeviceType, device_type=0x002B):
    """Fan."""

    clusters = {
        all_clusters.Identify,
        all_clusters.Descriptor,
        all_clusters.Groups,
        all_clusters.FanControl,
    }


class CastingVideoPlayer(DeviceType, device_type=0x0023):
    """Casting Video Player."""

    clusters = {
        all_clusters.Descriptor,
        all_clusters.MediaPlayback,
        all_clusters.KeypadInput,
        all_clusters.ApplicationLauncher,
        all_clusters.MediaInput,
        all_clusters.OnOff,
        all_clusters.Channel,
        all_clusters.AudioOutput,
        all_clusters.LowPower,
        all_clusters.WakeOnLan,
        all_clusters.TargetNavigator,
        all_clusters.AccountLogin,
        all_clusters.ContentLauncher,
    }


class BasicVideoPlayer(DeviceType, device_type=0x0028):
    """Basic Video Player."""

    clusters = {
        all_clusters.Descriptor,
        all_clusters.MediaPlayback,
        all_clusters.KeypadInput,
        all_clusters.MediaInput,
        all_clusters.OnOff,
        all_clusters.Channel,
        all_clusters.AudioOutput,
        all_clusters.LowPower,
        all_clusters.WakeOnLan,
        all_clusters.TargetNavigator,
    }


class CastingVideoClient(DeviceType, device_type=0x0029):
    """Casting Video Client."""

    clusters = {
        all_clusters.Descriptor,
        all_clusters.Binding,
        all_clusters.MediaPlayback,
        all_clusters.ContentLauncher,
        all_clusters.KeypadInput,
        all_clusters.AccountLogin,
        all_clusters.OnOff,
        all_clusters.LevelControl,
        all_clusters.WakeOnLan,
        all_clusters.Channel,
        all_clusters.TargetNavigator,
        all_clusters.MediaInput,
        all_clusters.LowPower,
        all_clusters.AudioOutput,
        all_clusters.ApplicationLauncher,
        all_clusters.ApplicationBasic,
    }


class VideoRemoteControl(DeviceType, device_type=0x002A):
    """Video Remote Control."""

    clusters = {
        all_clusters.Descriptor,
        all_clusters.Binding,
        all_clusters.MediaPlayback,
        all_clusters.ContentLauncher,
        all_clusters.KeypadInput,
        all_clusters.AccountLogin,
        all_clusters.OnOff,
        all_clusters.LevelControl,
        all_clusters.WakeOnLan,
        all_clusters.Channel,
        all_clusters.TargetNavigator,
        all_clusters.MediaInput,
        all_clusters.LowPower,
        all_clusters.AudioOutput,
        all_clusters.ApplicationLauncher,
    }


class Speaker(DeviceType, device_type=0x0022):
    """Speaker."""

    clusters = {
        all_clusters.Identify,
        all_clusters.Descriptor,
        all_clusters.OnOff,
        all_clusters.LevelControl,
    }


class ContentApp(DeviceType, device_type=0x0024):
    """Content App."""

    clusters = {
        all_clusters.Identify,
        all_clusters.Descriptor,
        all_clusters.ApplicationBasic,
        all_clusters.KeypadInput,
        all_clusters.ApplicationLauncher,
        all_clusters.AccountLogin,
        all_clusters.ContentLauncher,
        all_clusters.MediaPlayback,
        all_clusters.TargetNavigator,
        all_clusters.Channel,
    }


class ModeSelect(DeviceType, device_type=0x0027):
    """Mode Select."""

    clusters = {
        all_clusters.Identify,
        all_clusters.Descriptor,
        all_clusters.ModeSelect,
    }


class AllClustersAppServerExample(DeviceType, device_type=0x0000):
    """All-clusters-app Server Example."""

    clusters = {
        all_clusters.Identify,
        all_clusters.Descriptor,
        all_clusters.Binding,
        all_clusters.BarrierControl,
        all_clusters.ColorControl,
        all_clusters.DoorLock,
        all_clusters.Groups,
        all_clusters.LevelControl,
        all_clusters.OnOff,
        all_clusters.Scenes,
        all_clusters.TemperatureMeasurement,
    }


class SecondaryNetworkCommissioningDeviceType(DeviceType, device_type=0xF002):
    """Secondary Network Commissioning Device Type."""

    clusters = {
        all_clusters.NetworkCommissioning,
        all_clusters.Descriptor,
    }
