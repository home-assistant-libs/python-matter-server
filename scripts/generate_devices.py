import pathlib

import black
import xmltodict

REPO_ROOT = pathlib.Path(__file__).parent.parent

CHIP_ROOT = REPO_ROOT / "../connectedhomeip"
DEVICE_XML = CHIP_ROOT / "src/app/zap-templates/zcl/data-model/chip/matter-devices.xml"

OUTPUT_PYTHON = REPO_ROOT / "matter_server/vendor/device_types.py"


def gen_cls_name(name: str):
    # Convert uppercase words to titlecase
    name = "".join(
        # Don't mess up wifi name
        part if part == "WiFi" else part[0].upper() + part[1:].lower()
        for part in name.split(" ")
    )

    new_name = []

    next_upper = False
    for char in name:
        if char in ("-", "/"):
            next_upper = True
            continue
        elif next_upper:
            char = char.upper()
            next_upper = False

        new_name.append(char)

    return "".join(new_name)


def main():
    data = xmltodict.parse(DEVICE_XML.read_text())
    output = [
        """
from __future__ import annotations

import typing

from .chip.clusters import Objects as all_clusters

ALL_TYPES: dict[int, type["DeviceType"]] = {}



class DeviceType:
    \"""Base class for Matter device types.\"""

    device_type: int
    clusters: set[type[all_clusters.Cluster]]

    def __init_subclass__(cls, *, device_type: int, **kwargs: typing.Any) -> None:
        \"""Register a subclass.\"""
        super().__init_subclass__(**kwargs)
        cls.device_type = device_type
        ALL_TYPES[device_type] = cls

"""
    ]

    # Temporary: fan is missing from matter_devices.xml. Inject it after thermostat
    insert_idx = (
        next(
            idx
            for idx, device in enumerate(data["configurator"]["deviceType"])
            if device["typeName"] == "Matter Thermostat"
        )
        + 1
    )
    data["configurator"]["deviceType"].insert(
        insert_idx,
        {
            "typeName": "Matter Fan",
            "deviceId": {"#text": "0x002B"},
            "clusters": {
                "include": [
                    {"@cluster": "Identify", "@server": "true"},
                    {"@cluster": "Groups", "@server": "true"},
                    {"@cluster": "Fan Control", "@server": "true"},
                ]
            },
        },
    )

    for device in data["configurator"]["deviceType"]:
        name = device["typeName"]

        if not name.startswith("Matter "):
            print("Unexpected: device doesn't start wtih Matter. Skipping")
            continue

        name = name[len("Matter ") :]

        print(name, device["deviceId"]["#text"])

        clusters = device["clusters"]["include"]
        if not isinstance(clusters, list):
            clusters = [clusters]

        for cluster in clusters:
            print(cluster["@cluster"])

        print()

        if not clusters:
            output_clusters = "set()"
        else:
            output_clusters = (
                "{"
                + ",".join(
                    f"all_clusters.{gen_cls_name(cluster['@cluster'])}"
                    for cluster in clusters
                    # It's a server cluster
                    if cluster["@server"] == "true"
                    # It's optional server cluster
                    or cluster["@serverLocked"] == "false"
                )
                + ",}"  # extra comma to force black to do a cluster per line
            )

        output.append(
            """

class {cls_name}(DeviceType, device_type={device_id}):
    \"""{device_name}.\"""

    clusters = {output_clusters}


""".format(
                device_name=name,
                cls_name=gen_cls_name(name),
                device_id=device["deviceId"]["#text"],
                output_clusters=output_clusters,
            )
        )

    formatted = black.format_str("\n\n".join(output), mode=black.Mode())
    OUTPUT_PYTHON.write_text(formatted)


if __name__ == "__main__":
    main()
