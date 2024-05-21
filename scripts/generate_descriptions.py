"""Generate descriptions.json for the dashboard."""

# NOTE: we need to do a wildcard import from models.clusters to include all
# custom clusters in the output defined in that file
# pylint: disable=wildcard-import, unused-wildcard-import, invalid-name
import pathlib
from typing import Any, Final

from chip.clusters.ClusterObjects import (
    ALL_ATTRIBUTES,
    ALL_CLUSTERS,
    Cluster,
    ClusterAttributeDescriptor,
)

from matter_server.client.models.device_types import (
    ALL_TYPES as DEVICE_TYPES,
    DeviceType,
)
from matter_server.common.helpers.json import json_dumps

OUTPUT_FILE: Final[pathlib.Path] = (
    pathlib.Path(__file__)
    .parent.resolve()
    .parent.resolve()
    .joinpath("dashboard/src/client/models/descriptions.ts")
)


def generate_device_type_description(device_type: DeviceType) -> dict[str, Any]:
    """Generate a (human readable) description for a device type as dict."""
    return {
        "id": device_type.device_type,
        "label": (device_type.__doc__ or device_type.__name__).replace(".", ""),
        "clusters": {x.id for x in device_type.clusters},
    }


def create_pretty_name_for_type(_type: type) -> str:
    """Create pretty name for Python type annotation."""
    return (
        str(_type)
        .replace("<", "")
        .replace(">", "")
        .replace("typing.", "")
        .replace("chip.tlv.", "")
        .replace("chip.clusters.Types.", "")
        .replace("chip.clusters.Objects.", "")
        .replace("class", "")
        .replace("'", "")
        .strip()
    )


def generate_attribute_description(
    attribute: ClusterAttributeDescriptor,
) -> dict[str, Any]:
    """Generate a (human readable) description for a ClusterAttribute as dict."""
    return {
        "id": attribute.attribute_id,
        "cluster_id": attribute.cluster_id,
        "label": attribute.attribute_type.Label or attribute.__name__,
        "type": create_pretty_name_for_type(attribute.attribute_type.Type),
    }


def generate_cluster_description(cluster: Cluster) -> dict[str, Any]:
    """Generate a (human readable) description for a Cluster as dict."""
    return {
        "id": cluster.id,
        "label": cluster.__name__,
        "attributes": {
            attribute_id: generate_attribute_description(attribute)
            for attribute_id, attribute in ALL_ATTRIBUTES[cluster.id].items()
        },
    }


device_types = {
    dev_type_id: generate_device_type_description(dev_type)
    for dev_type_id, dev_type in DEVICE_TYPES.items()
}

clusters = {
    cluster_id: generate_cluster_description(cluster)
    for cluster_id, cluster in ALL_CLUSTERS.items()
}

output = """
/* Descriptions for SDK Objects. This file is auto generated, do not edit. */

export interface DeviceType {
  id: number;
  label: string;
  clusters: number[];
}

export interface ClusterAttributeDescription {
  id: number;
  cluster_id: number;
  label: string;
  type: string;
}

export interface ClusterDescription {
  id: number;
  label: string;
  attributes: { [attribute_id: string]: ClusterAttributeDescription }
}

"""
output += f"""
export const device_types: Record<number, DeviceType> = {json_dumps(device_types)}

export const clusters: Record<number, ClusterDescription> = {json_dumps(clusters)}

"""

OUTPUT_FILE.write_text(output, encoding="utf-8")
