"""Helpers to work with (de)serializing of json."""

from base64 import b64encode
from dataclasses import is_dataclass
from typing import Any

from chip.clusters.Attribute import ValueDecodeFailure
from chip.clusters.Types import Nullable
from chip.tlv import float32, uint
import orjson

from .util import dataclass_to_dict

JSON_ENCODE_EXCEPTIONS = (TypeError, ValueError)
JSON_DECODE_EXCEPTIONS = (orjson.JSONDecodeError,)


def json_encoder_default(obj: Any) -> Any:
    """Convert Special objects.

    Hand other objects to the original method.
    """
    if getattr(obj, "do_not_serialize", None):
        return None
    if isinstance(obj, ValueDecodeFailure):
        return None
    if isinstance(obj, (set, tuple)):
        return list(obj)
    if isinstance(obj, float32):
        return float(obj)
    if isinstance(obj, uint):
        return int(obj)
    if hasattr(obj, "as_dict"):
        return obj.as_dict()
    if is_dataclass(obj):
        return dataclass_to_dict(obj)
    if isinstance(obj, Nullable):
        return None
    if isinstance(obj, bytes):
        return b64encode(obj).decode("utf-8")
    if isinstance(obj, Exception):
        return str(obj)
    if type(obj) == type:
        return f"{obj.__module__}.{obj.__qualname__}"

    raise TypeError


def json_dumps(data: Any) -> str:
    """Dump json string."""
    return orjson.dumps(
        data,
        option=orjson.OPT_NON_STR_KEYS
        | orjson.OPT_INDENT_2
        | orjson.OPT_PASSTHROUGH_DATACLASS,
        default=json_encoder_default,
    ).decode("utf-8")


json_loads = orjson.loads
