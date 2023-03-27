"""Script to beautify diagnostics output."""
import json
import sys

import yaml
from chip.clusters.ClusterObjects import ALL_ATTRIBUTES, ALL_CLUSTERS

from matter_server.client.models.device_types import ALL_TYPES


def main():
    """Run the script."""
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <diagnostics_file.json>")
        sys.exit(1)

    with open(sys.argv[1]) as f:
        data = json.load(f)

    nodes = [data["data"]["node"]] if "node" in data["data"] else data["data"]["server"]["nodes"]

    for node in nodes:
        process_node(node)

    yaml.safe_dump(data, sys.stdout, indent=2, sort_keys=False)


def process_node(node):
    """Process a node."""
    endpoints = {}
    cluster_warn = set()

    for attr_path, value in node["attributes"].items():
        endpoint_id, cluster_id, attr_id = attr_path.split("/")
        cluster_id = int(cluster_id)
        endpoint_id = int(endpoint_id)
        attr_id = int(attr_id)

        if cluster_id in ALL_CLUSTERS:
            cluster_name = (
                f"{ALL_CLUSTERS[cluster_id].__name__} ({cluster_id} / 0x{cluster_id:04x})"
            )
        else:
            if cluster_id not in cluster_warn:
                print(f"Unknown cluster ID: {cluster_id}")
                cluster_warn.add(cluster_id)
            cluster_name = f"{cluster_id} (unknown)"

        if cluster_id in ALL_ATTRIBUTES and attr_id in ALL_ATTRIBUTES[cluster_id]:
            attr_name = (
                f"{ALL_ATTRIBUTES[cluster_id][attr_id].__name__} ({attr_id} / 0x{attr_id:04x})"
            )
        else:
            if cluster_id not in cluster_warn:
                print(
                    "Unknown attribute ID: {} in cluster {} ({})".format(
                        attr_id, cluster_name, cluster_id
                    )
                )
            attr_name = f"{attr_id} (unknown)"

        if endpoint_id not in endpoints:
            endpoints[endpoint_id] = {}

        if cluster_name not in endpoints[endpoint_id]:
            endpoints[endpoint_id][cluster_name] = {}

        endpoints[endpoint_id][cluster_name][attr_name] = value

    # Augment device types
    for endpoint in endpoints.values():
        if not (descriptor_cls := endpoint.get("Descriptor (29 / 0x001d)")):
            continue

        if not (device_types := descriptor_cls.get("DeviceTypeList (0 / 0x0000)")):
            continue

        for device_type in device_types:
            device_type_id = device_type["type"]
            if device_type_id in ALL_TYPES:
                device_type_name = ALL_TYPES[device_type_id].__name__
            else:
                device_type_name = f"{device_type} (unknown)"

            device_type["name"] = device_type_name
            device_type["hex"] = f"0x{device_type_id:04x}"

    node["attributes"] = {
        f"Endpoint {endpoint_id}": clusters for endpoint_id, clusters in endpoints.items()
    }


main()
