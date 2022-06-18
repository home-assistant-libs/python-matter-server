"""Show mappings for given JSON."""

import dataclasses
import json
import logging
import os
import pathlib
import sys
from unittest.mock import Mock

from custom_components.matter_experimental.device_platform import DEVICE_PLATFORM
from matter_server.client.model.device import MatterDevice
from matter_server.client.model.node import MatterNode
from matter_server.common import json_utils


def resolve_input():
    if len(sys.argv) < 2:
        print("Pass in path to JSON file containing single node or HA storage")
        sys.exit(1)

    path = sys.argv[1]

    return (pathlib.Path(os.getcwd()) / path).read_text()


def print_node(node: MatterNode):
    print(node)
    first = True
    for device in node.devices:
        if first:
            first = False
        else:
            print()
        print_device(device)


def print_device(device: MatterDevice):
    created = False
    print(f"  {device}")

    for platform, devices in DEVICE_PLATFORM.items():
        device_mappings = devices.get(device.device_type)

        if device_mappings is None:
            continue

        if not isinstance(device_mappings, list):
            device_mappings = [device_mappings]

        for device_mapping in device_mappings:
            created = True
            print(f"    - Platform: {platform}")

            for key, value in sorted(dataclasses.asdict(device_mapping).items()):
                if value is None:
                    continue
                if key == "entity_cls":
                    value = value.__name__

                if key != "subscribe_attributes":
                    print(f"      {key}: {value}")
                    continue

                print("      Subscriptions:")

                for sub in value:
                    print(f"       - {sub.__qualname__}")

                # Try instantiating to ensure the device mapping doesn't crash
                device_mapping.entity_cls(device, device_mapping)

    # Do not warng on root node
    if not created:
        print("  ** WARNING: NOT MAPPED IN HOME ASSISTANT")


def main():
    raw_data = resolve_input()
    data = json.loads(raw_data, cls=json_utils.CHIPJSONDecoder)

    # This is a HA storage file. Extract nodes
    if "key" in data and data["key"].startswith("matter_experimental_"):
        nodes = [d for d in data["data"]["nodes"].values() if d is not None]
    else:
        nodes = [data]

    first = True

    mock_matter = Mock(adapter=Mock(logger=logging.getLogger("show_mappings")))

    for node_data in nodes:
        if first:
            first = False
        else:
            print()
            print()

        print_node(MatterNode(mock_matter, node_data))


if __name__ == "__main__":
    main()
