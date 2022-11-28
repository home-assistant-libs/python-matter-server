"""Helpers to work with (de)serializing of json."""

from typing import Any

from chip.clusters.Types import Nullable, NullValue
import orjson

JSON_ENCODE_EXCEPTIONS = (TypeError, ValueError)
JSON_DECODE_EXCEPTIONS = (orjson.JSONDecodeError,)


def json_encoder_default(obj: Any) -> Any:
    """
    Convert Special objects.
    Hand other objects to the original method.
    """
    if isinstance(obj, (set, tuple)):
        return list(obj)
    if isinstance(obj, float):
        return float(obj)
    if hasattr(obj, "as_dict"):
        return obj.as_dict()
    if isinstance(obj, Nullable):
        return None

    raise TypeError


def json_dumps(data: Any) -> str:
    """Dump json string."""
    return orjson.dumps(
        data, option=orjson.OPT_NON_STR_KEYS, default=json_encoder_default
    ).decode("utf-8")


json_loads = orjson.loads
