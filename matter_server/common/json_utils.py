import base64
import json
import sys
from enum import Enum

# Compatible both with vendorized and not-vendorized
try:
    from chip.clusters import Objects as Clusters
    from chip.clusters.Types import Nullable
except ImportError:
    from ..vendor.chip.clusters import Objects as Clusters
    from ..vendor.chip.clusters.Types import Nullable


CLUSTER_TYPE_NAMESPACE = "chip.clusters.Objects"


class CHIPJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Nullable):
            return None
        elif isinstance(obj, type):
            # Maybe we should restrict this to CHIP cluster types (see deserialization?)
            return {"_class": f"{obj.__module__}.{obj.__qualname__}"}
        elif isinstance(obj, Enum):
            # Works for chip.clusters.Attributes.EventPriority,
            # might need more sophisticated solution for other Enums
            # Also, deserialization?
            return obj.value
        elif isinstance(obj, bytes):
            return {"_type": "bytes", "value": base64.b64encode(obj).decode("utf-8") }
        # if is_dataclass(obj):
        #     return asdict(obj)
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)


class CHIPJSONDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def _get_class(self, type: str):
        if not type.startswith(CLUSTER_TYPE_NAMESPACE):
            raise TypeError("Only CHIP cluster objects supported")

        cluster_type = type.removeprefix(f"{CLUSTER_TYPE_NAMESPACE}.")

        cluster_cls = Clusters
        for cluster_subtype in cluster_type.split("."):
            cluster_cls = getattr(cluster_cls, cluster_subtype)

        return cluster_cls

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
