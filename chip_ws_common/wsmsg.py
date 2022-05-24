import json
import sys
from dataclasses import asdict, dataclass, is_dataclass

import chip.clusters.Objects

CLUSTER_TYPE_NAMESPACE = "chip.clusters.Objects"


class WSEncoder(json.JSONEncoder):
     def default(self, obj):
        if is_dataclass(obj):
            return asdict(obj)
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)


class WSDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)
        
    def object_hook(self, obj: dict):
        _type = obj.get('_type')
        if _type is None:
            return obj

        if not _type.startswith(CLUSTER_TYPE_NAMESPACE):
            raise TypeError("Only CHIP cluster objects supported")

        cluster_type = _type.removeprefix(f"{CLUSTER_TYPE_NAMESPACE}.")
        # Delete the `_type` key as it isn't used in the dataclasses
        del obj['_type']
        
        cluster_cls = sys.modules[CLUSTER_TYPE_NAMESPACE]
        for cluster_subtype in cluster_type.split("."):
            print(cluster_subtype)
            cluster_cls = getattr(cluster_cls, cluster_subtype)
        
        return cluster_cls(**obj)

@dataclass
class WSCommandMessage:
    command: str
    args: dict
