"""Utils for Matter server (and client)."""
from __future__ import annotations

from base64 import b64encode
from dataclasses import MISSING, asdict, fields, is_dataclass
from datetime import datetime
from enum import Enum
from functools import cache
from importlib.metadata import PackageNotFoundError, version as pkg_version
import logging
import platform
from types import NoneType, UnionType
from typing import Any, TypeVar, Union, get_args, get_origin, get_type_hints

from chip.clusters.Types import Nullable, NullValue
from chip.tlv import float32, uint

_T = TypeVar("_T")

CHIP_CLUSTERS_PKG_NAME = "home-assistant-chip-clusters"
CHIP_CORE_PKG_NAME = "home-assistant-chip-core"


def create_attribute_path(endpoint: int, cluster_id: int, attribute_id: int) -> str:
    """
    Create path/identifier for an Attribute.

    Returns same output as `Attribute.AttributePath`
    endpoint/cluster_id/attribute_id
    """
    return f"{endpoint}/{cluster_id}/{attribute_id}"


def parse_attribute_path(attribute_path: str) -> tuple[int, int, int]:
    """Parse AttributePath string into endpoint_id, cluster_id, attribute_id"""
    endpoint_id_str, cluster_id_str, attribute_id_str = attribute_path.split("/")
    return (int(endpoint_id_str), int(cluster_id_str), int(attribute_id_str))


def dataclass_to_dict(obj_in: object, skip_none: bool = False) -> dict:
    """Convert dataclass instance to dict, optionally skip None values."""
    if skip_none:
        dict_obj = asdict(
            obj_in, dict_factory=lambda x: {k: v for (k, v) in x if v is not None}
        )
    else:
        dict_obj = asdict(obj_in)

    def _convert_value(value: Any) -> Any:
        """Do some common conversions."""
        if isinstance(value, list):
            return [_convert_value(x) for x in value]
        if isinstance(value, Nullable) or value == NullValue:
            return None
        if isinstance(value, dict):
            return _clean_dict(value)
        if isinstance(value, Enum):
            return value.value
        if isinstance(value, bytes):
            return b64encode(value).decode()
        if isinstance(value, float32):
            return float(value)
        if type(value) == type:
            return f"{value.__module__}.{value.__qualname__}"
        if isinstance(value, Exception):
            return None
        return value

    def _clean_dict(_dict_obj: dict) -> dict:
        _final = {}
        for key, value in _dict_obj.items():
            if isinstance(key, int):
                key = str(key)
            _final[key] = _convert_value(value)
        return _final

    return _clean_dict(dict_obj)


def parse_utc_timestamp(datetime_string: str) -> datetime:
    """Parse datetime from string."""
    return datetime.fromisoformat(datetime_string.replace("Z", "+00:00"))


def parse_value(name: str, value: Any, value_type: Any, default: Any = MISSING) -> Any:
    """Try to parse a value from raw (json) data and type annotations."""

    if isinstance(value_type, str):
        # this shouldn't happen, but just in case
        value_type = get_type_hints(value_type, globals(), locals())

    # always prefer classes that have a from_dict / FromDict
    if isinstance(value, dict):
        if hasattr(value_type, "from_dict"):
            return value_type.from_dict(value)
        if hasattr(value_type, "FromDict"):
            return value_type.FromDict(value)

    if value is None and not isinstance(default, type(MISSING)):
        return default
    if value is None and value_type is NoneType:
        return None
    if is_dataclass(value_type) and isinstance(value, dict):
        return dataclass_from_dict(value_type, value)  # type: ignore[arg-type]
    origin = get_origin(value_type)
    if origin is list:
        return [
            parse_value(name, subvalue, get_args(value_type)[0])
            for subvalue in value
            if subvalue is not None
        ]
    # handle dictionary where we should inspect all values
    elif origin is dict:
        subkey_type = get_args(value_type)[0]
        subvalue_type = get_args(value_type)[1]
        return {
            parse_value(subkey, subkey, subkey_type): parse_value(
                f"{subkey}.value", subvalue, subvalue_type
            )
            for subkey, subvalue in value.items()
        }
    # handle Union type
    elif origin is Union or origin is UnionType:
        # try all possible types
        sub_value_types = get_args(value_type)
        for sub_arg_type in sub_value_types:
            if value is NoneType and sub_arg_type is NoneType:
                return value
            # try them all until one succeeds
            try:
                return parse_value(name, value, sub_arg_type)
            except (KeyError, TypeError, ValueError):
                pass
        # if we get to this point, all possibilities failed
        # find out if we should raise or log this
        err = (
            f"Value {value} of type {type(value)} is invalid for {name}, "
            f"expected value of type {value_type}"
        )
        if NoneType not in sub_value_types:
            # raise exception, we have no idea how to handle this value
            raise TypeError(err)
        # failed to parse the (sub) value but None allowed, log only
        logging.getLogger(__name__).warn(err)
        return None
    elif origin is type:
        return get_type_hints(value, globals(), locals())
    if value_type is Any:
        return value
    if value is None and value_type is not NoneType:
        raise KeyError(f"`{name}` of type `{value_type}` is required.")

    try:
        if issubclass(value_type, Enum):  # type: ignore[arg-type]
            return value_type(value)  # type: ignore[operator]
        if issubclass(value_type, datetime):  # type: ignore[arg-type]
            return parse_utc_timestamp(value)
    except TypeError:
        # happens if value_type is not a class
        pass

    # the value type itself is literally type, meaning we should treat the value string
    # as the actual type - TODO: Remove when we changed the datamodels
    if value_type is type:
        return eval(value)

    # common type conversions (e.g. int as string)
    if value_type is float and isinstance(value, int):
        return float(value)
    if value_type is int and isinstance(value, str) and value.isnumeric():
        return int(value)

    # Matter SDK specific types
    if value_type is uint and (
        isinstance(value, int) or (isinstance(value, str) and value.isnumeric())
    ):
        return uint(value)
    if value_type is float32 and (
        isinstance(value, float) or (isinstance(value, str) and value.isnumeric())
    ):
        return float32(value)

    # If we reach this point, we could not match the value with the type and we raise
    if not isinstance(value, value_type):  # type: ignore[arg-type]
        raise TypeError(
            f"Value {value} of type {type(value)} is invalid for {name}, "
            f"expected value of type {value_type}"
        )
    return value


def dataclass_from_dict(cls: type[_T], dict_obj: dict, strict: bool = False) -> _T:
    """
    Create (instance of) a dataclass by providing a dict with values.

    Including support for nested structures and common type conversions.
    If strict mode enabled, any additional keys in the provided dict will result in a KeyError.
    """
    if strict:
        extra_keys = dict_obj.keys() - set([f.name for f in fields(cls)])
        if extra_keys:
            raise KeyError(
                "Extra key(s) %s not allowed for %s"
                % (",".join(extra_keys), (str(cls)))
            )
    type_hints = get_type_hints(cls)
    return cls(
        **{
            field.name: parse_value(
                f"{cls.__name__}.{field.name}",
                dict_obj.get(field.name),
                type_hints[field.name],
                field.default,
            )
            for field in fields(cls)
            if field.init
        }
    )


def package_version(pkg_name: str) -> str:
    """
    Return the version of an installed package.

    Will return `0.0.0` if the package is not found.
    """
    try:
        installed_version = pkg_version(pkg_name)
        if installed_version is None:
            return "0.0.0"  # type: ignore[unreachable]
        return installed_version
    except PackageNotFoundError:
        return "0.0.0"


@cache
def chip_clusters_version() -> str:
    """Return the version of the CHIP SDK (clusters package) that is installed."""
    return package_version(CHIP_CLUSTERS_PKG_NAME)


@cache
def chip_core_version() -> str:
    """Return the version of the CHIP SDK (core package) that is installed."""
    if platform.system() == "Darwin":
        # TODO: Fix this once we can install our own wheels on macos.
        return chip_clusters_version()
    return package_version(CHIP_CORE_PKG_NAME)
