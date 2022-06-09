"""List all devices not mapped in the custom component.

Run with python3 -m scripts.list_unmapped_devices
"""
from custom_components.matter_experimental.device_platform import DEVICE_PLATFORM
from matter_server.vendor import device_types


IGNORE_DEVICES = {
    device_types.AllClustersAppServerExample,
    device_types.Bridge,
    device_types.BridgedDevice,
    device_types.ColorDimmerSwitch,
    device_types.ControlBridge,
    device_types.DimmerSwitch,
    device_types.DoorLockController,
    device_types.OnOffLightSwitch,
    device_types.OnOffSensor,
    device_types.OrphanClusters,
    device_types.OtaProvider,
    device_types.OtaRequestor,
    device_types.PumpController,
    device_types.RootNode,
    device_types.SecondaryNetworkCommissioningDeviceType,
    device_types.WindowCoveringController,
}


def main():
    for device_cls in device_types.ALL_TYPES.values():
        if device_cls in IGNORE_DEVICES:
            continue

        found = False
        for device_mappings in DEVICE_PLATFORM.values():
            if device_cls in device_mappings:
                found = True
                break

        if not found:
            print(device_cls.__name__)


if __name__ == "__main__":
    main()
