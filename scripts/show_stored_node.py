"""Show mappings for given JSON."""

import dataclasses
import json
import os
import pathlib
import sys

from custom_components.matter_experimental.device_platform import DEVICE_PLATFORM
from matter_server.client.model.device import MatterDevice
from matter_server.client.model.node import MatterNode
from matter_server.common import json_utils

from tests.test_utils.mock_matter import get_mock_matter


class PrintButFirst:
    first = True

    def __init__(self, lines=1) -> None:
        self.lines = lines

    def __call__(self):
        if self.first:
            self.first = False
        else:
            for _ in range(self.lines):
                print()


def resolve_input():
    if len(sys.argv) < 2:
        print("Pass in path to JSON file containing single node or HA storage")
        sys.exit(1)

    path = sys.argv[1]

    return (pathlib.Path(os.getcwd()) / path).read_text()


def print_node(node: MatterNode):
    print(node)
    item_space_printer = PrintButFirst()

    for device in node.devices:
        item_space_printer()
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

                if key == "entity_description":
                    print(f"      {key}:")
                    for ed_key, ed_value in sorted(value.items()):
                        if ed_value is None or (  # filter out default values
                            device_mapping.entity_description.__dataclass_fields__[
                                ed_key
                            ].default
                            is ed_value
                        ):
                            continue
                        print(f"        {ed_key}: {ed_value}")
                    continue

                if key == "entity_cls":
                    value = value.__name__

                if key != "subscribe_attributes":
                    print(f"      {key}: {value}")
                    continue

                print("      subscriptions:")

                for sub in value:
                    print(f"       - {sub.__qualname__}")

                # Try instantiating to ensure the device mapping doesn't crash
                device_mapping.entity_cls(device, device_mapping)

    # Do not warng on root node
    if not created:
        print("    ** WARNING: NOT MAPPED IN HOME ASSISTANT")


def parse_data(data):
    return json.loads(data, cls=json_utils.CHIPJSONDecoder)


def nodes_from_data(data):
    # This is a HA storage file. Extract nodes
    if "key" in data and data["key"].startswith("matter_experimental_"):
        return [d for d in data["data"]["nodes"].values() if d is not None]

    return [data]


def get_nodes():
    mock_matter = get_mock_matter()

    return [
        MatterNode(mock_matter, node_data)
        for node_data in nodes_from_data(parse_data(resolve_input()))
    ]


def main():
    item_space_printer = PrintButFirst(2)

    for node in get_nodes():
        item_space_printer()
        print_node(node)


if __name__ == "__main__":
    main()
