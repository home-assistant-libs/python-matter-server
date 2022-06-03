import base64
import json
import sys
from dataclasses import asdict, is_dataclass
from enum import Enum
from types import ModuleType

import matter_server.common.model
from matter_server.common.model.message import Message

# Compatible both with vendorized and not-vendorized
try:
    from chip.clusters import Objects as Clusters
    from chip.clusters.Types import Nullable
    from chip.interaction_model import InteractionModelError
except ImportError:
    from ..vendor.chip.clusters import Objects as Clusters
    from ..vendor.chip.clusters.Types import Nullable


MATTER_SERVER_NAMESPACE = "matter_server.common.model"
CLUSTER_TYPE_NAMESPACE = "chip.clusters.Objects"
CLUSTER_TYPE_VENDORIZED_NAMESPACE = "matter_server.vendor"


class CHIPJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Nullable):
            return None
        elif isinstance(obj, Exception):
            # Work around for InteractionModelError/ValueError exceptions currently experiencing in
            # the ThreadNetworkDiagnostics Cluster
            return str(obj)
        elif isinstance(obj, type):
            namespace = obj.__module__
            if namespace.startswith(CLUSTER_TYPE_VENDORIZED_NAMESPACE):
                namespace = namespace.removeprefix(f"{CLUSTER_TYPE_VENDORIZED_NAMESPACE}.")
            # Maybe we should restrict this to CHIP cluster types (see deserialization?)
            return {"_class": f"{namespace}.{obj.__qualname__}"}
        elif isinstance(obj, Enum):
            # Works for chip.clusters.Attributes.EventPriority,
            # might need more sophisticated solution for other Enums
            # Also, deserialization?
            return obj.value
        elif isinstance(obj, bytes):
            return {"_type": "bytes", "value": base64.b64encode(obj).decode("utf-8") }

        if is_dataclass(obj):
            result = asdict(obj)
            cls = type(obj)
            result["_type"] = f"{cls.__module__}.{cls.__qualname__}"
            return result

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
            return self._get_class_from_module(matter_server.common.model, matter_server_type)
        else:
            raise TypeError("Only CHIP cluster objects supported")

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
