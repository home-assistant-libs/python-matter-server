"""List all devices not mapped in the custom component.

Run with python3 -m scripts.list_unmapped_devices
"""
from custom_components.matter_experimental.device_platform import DEVICE_PLATFORM
from matter_server.client.model.device import DEVICE_TYPES
from matter_server.client.model import devices


IGNORE_DEVICES = {
    devices.OrphanClusters,
    devices.RootNode,
    devices.OtaRequestor,
    devices.OtaProvider,
    devices.Bridge,
    devices.BridgedDevice,
    devices.ControlBridge,
    devices.AllClustersAppServerExample,
    devices.SecondaryNetworkCommissioningDeviceType,
}


def main():
    for device_cls in DEVICE_TYPES.values():
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
