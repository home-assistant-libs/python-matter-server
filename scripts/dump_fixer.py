"""Help patch bad dumps.

When a dump doesn't match the expected TLV data from the Matter SDK,
we don't dump it as a correct Matter class, but a collection of TLVValues.

This script will look up that data and try to re-construct the data.
"""
import json
from pprint import pprint

from matter_server.common import json_utils
from matter_server.vendor.chip.clusters import Objects as all_clusters

from .show_stored_node import get_nodes, PrintButFirst


def process_node(node):
    print(f"Node {node.node_id}")
    for endpoint_id, endpoint_data in node.raw_data["attributes"].items():
        for cluster_name, cluster_info in endpoint_data.items():
            # It's a dict if it couldn't parse it.
            if not isinstance(cluster_info, dict):
                continue

            print(
                f"** Found unprocessed cluster at endpoint {endpoint_id}: {cluster_name}"
            )
            print(f"Reason: {cluster_info['Reason']}")
            print()
            cluster_cls = getattr(all_clusters, cluster_name)
            field_lookup = {
                str(desc.Tag): desc.Label for desc in cluster_cls.descriptor.Fields
            }

            fixed = {}
            bad = {}

            for field_id, field_data in cluster_info["TLVValue"].items():
                if field_id not in field_lookup:
                    bad[field_id] = field_data
                    continue

                if isinstance(field_data, dict) and "TLVValue" in field_data:
                    bad[field_lookup[field_id]] = field_data
                else:
                    fixed[field_lookup[field_id]] = field_data

            fixed["_type"] = f"chip.clusters.Objects.{cluster_name}"

            print(json.dumps(fixed, cls=json_utils.CHIPJSONEncoder, indent=2))

            if bad:
                print()
                print("Bad fields:")
                pprint(bad)

            print()


def main():
    item_space_printer = PrintButFirst(2)

    for node in get_nodes():
        item_space_printer()
        process_node(node)


if __name__ == "__main__":
    main()
