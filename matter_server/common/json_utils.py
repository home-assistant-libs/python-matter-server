import base64
import copy
from dataclasses import fields, is_dataclass
from enum import Enum
import json

import matter_server.common.model

# Compatible both with vendorized and not-vendorized
try:
    from chip.clusters import Objects as Clusters
    from chip.clusters.Types import Nullable
except ImportError:
    from ..vendor.chip.clusters import Objects as Clusters
    from ..vendor.chip.clusters.Types import Nullable

MATTER_SERVER_NAMESPACE = "matter_server.common.model"
CLUSTER_TYPE_NAMESPACE = "chip.clusters.Objects"
CLUSTER_ATTRIBUTE_NAMESPACE = "chip.clusters.Attribute"
CLUSTER_TYPE_VENDORIZED_NAMESPACE = "matter_server.vendor"


def strip_vendorized_namespace(namespace):
    if namespace.startswith(CLUSTER_TYPE_VENDORIZED_NAMESPACE):
        return namespace.removeprefix(f"{CLUSTER_TYPE_VENDORIZED_NAMESPACE}.")
    return namespace


# Copy of dataclasses._asdict_inner
def asdict_typed(obj, dict_factory):
    if is_dataclass(obj) and not isinstance(obj, type):
        cls = type(obj)
        result = []
        for f in fields(obj):
            value = asdict_typed(getattr(obj, f.name), dict_factory)
            result.append((f.name, value))
        # Add type information to prepare for serializing dataclasses
        result.append(
            (
                "_type",
                f"{strip_vendorized_namespace(cls.__module__)}.{cls.__qualname__}",
            )
        )
        return dict_factory(result)
    elif isinstance(obj, tuple) and hasattr(obj, "_fields"):
        return type(obj)(*[asdict_typed(v, dict_factory) for v in obj])
    elif isinstance(obj, (list, tuple)):
        return type(obj)(asdict_typed(v, dict_factory) for v in obj)
    elif isinstance(obj, dict):
        return type(obj)(
            (asdict_typed(k, dict_factory), asdict_typed(v, dict_factory))
            for k, v in obj.items()
        )
    else:
        return copy.deepcopy(obj)


class CHIPJSONEncoder(json.JSONEncoder):
    def _encode_dataclasses_and_dict_keys(self, obj):
        obj = asdict_typed(obj, dict)

        # Matter uses Cluster Attribute classes as dict keys.
        # Arbitrary types as not allowed by JSON encoder
        # Encode as string for now.
        if isinstance(obj, dict):
            return {
                k.__name__
                if isinstance(k, type)
                else k: self._encode_dataclasses_and_dict_keys(v)
                for k, v in obj.items()
            }
        return obj

    def encode(self, obj):
        obj = self._encode_dataclasses_and_dict_keys(obj)
        return json.JSONEncoder.encode(self, obj)

    def default(self, obj):
        if isinstance(obj, Nullable):
            return None
        elif isinstance(obj, Exception):
            # Work around for InteractionModelError/ValueError exceptions currently experiencing in
            # the ThreadNetworkDiagnostics Cluster
            return str(obj)
        elif isinstance(obj, type):
            namespace = strip_vendorized_namespace(obj.__module__)
            # Maybe we should restrict this to CHIP cluster types (see deserialization?)
            return {"_class": f"{namespace}.{obj.__qualname__}"}
        elif isinstance(obj, Enum):
            # Works for chip.clusters.Attributes.EventPriority,
            # might need more sophisticated solution for other Enums
            # Also, deserialization?
            return obj.value
        elif isinstance(obj, bytes):
            return {"_type": "bytes", "value": base64.b64encode(obj).decode("utf-8")}

        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)


class CHIPJSONDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def _get_class_from_module(self, cluster_cls, type: str):
        for cluster_subtype in type.split("."):
            cluster_cls = getattr(cluster_cls, cluster_subtype)

        return cluster_cls

    def _get_class(self, type: str):
        if type.startswith(CLUSTER_TYPE_NAMESPACE):
            cluster_type = type.removeprefix(f"{CLUSTER_TYPE_NAMESPACE}.")
            return self._get_class_from_module(Clusters, cluster_type)
        elif type.startswith(MATTER_SERVER_NAMESPACE):
            matter_server_type = type.removeprefix(f"{MATTER_SERVER_NAMESPACE}.")
            return self._get_class_from_module(
                matter_server.common.model, matter_server_type
            )
        elif type.startswith(CLUSTER_ATTRIBUTE_NAMESPACE):
            # TODO: How do we deal with that?
            # chip.clusters.Attribute.AsyncReadTransaction.ReadResponse
            return dict
        else:
            raise TypeError(
                f"Type {type} unsupported. Only CHIP cluster and Matter server types supported"
            )

    def object_hook(self, obj: dict):
        if type := obj.get("_type"):
            if type == "bytes":
                return base64.b64decode(obj["value"])
            else:
                cls = self._get_class(type)
                # Delete the `_type` key as it isn't used in the dataclasses
                del obj["_type"]
                return cls(**obj)
        elif cls := obj.get("_class"):
            return self._get_class(cls)

        return obj
