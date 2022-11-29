"""Utils for Matter server (and client)."""
from __future__ import annotations
from base64 import b64encode
from dataclasses import MISSING, asdict, dataclass, fields, is_dataclass
from datetime import date, datetime
from enum import Enum
from functools import cache
from importlib.metadata import PackageNotFoundError, version as pkg_version
import logging
import platform
from typing import Any, Dict, Optional, Set, Type, Union, get_args, get_origin

# the below imports are here to satisfy our dataclass from dict helper
# it needs to be able to instantiate common class instances from type hints
from chip.clusters import Cluster, ClusterObject, Objects
import chip
from ..models.node import MatterNode, MatterAttribute
from chip.clusters.Types import Nullable, NullValue
from chip.tlv import float32, uint
import pkg_resources


try:
    # python 3.10
    from types import NoneType
except:  # noqa
    # older python version
    NoneType = type(None)

CHIP_CLUSTERS_PKG_NAME = "home-assistant-chip-clusters"
CHIP_CORE_PKG_NAME = "home-assistant-chip-core"


def dataclass_to_dict(obj_in: dataclass, skip_none: bool = False) -> dict:
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

    def _clean_dict(_dict_obj: dict):
        final = {}
        for key, value in _dict_obj.items():
            if isinstance(key, int):
                key = str(key)
            final[key] = _convert_value(value)
        return final

    return _clean_dict(dict_obj)


def parse_utc_timestamp(datetimestr: str):
    """Parse datetime from string."""
    return datetime.fromisoformat(datetimestr.replace("Z", "+00:00"))


def parse_value(name: str, value: Any, value_type: Type | str, default: Any = MISSING):
    """Try to parse a value from raw (json) data and type definitions."""

    if isinstance(value_type, str):
        # type is provided as string
        if value_type == "type":
            return eval(value)
        value_type = eval(value_type)

    elif isinstance(value, dict):
        if hasattr(value_type, "from_dict"):
            return value_type.from_dict(value)
        if hasattr(value_type, "FromDict"):
            return value_type.FromDict(value)

    if value is None and not isinstance(default, type(MISSING)):
        return default
    if value is None and value_type is NoneType:
        return None
    if is_dataclass(value_type) and isinstance(value, dict):
        return dataclass_from_dict(value_type, value)
    origin = get_origin(value_type)
    if origin is list:
        return [
            parse_value(name, subval, get_args(value_type)[0])
            for subval in value
            if subval is not None
        ]
    if origin is dict:
        subkey_type = get_args(value_type)[0]
        subvalue_type = get_args(value_type)[1]
        return {
            parse_value(subkey, subkey, subkey_type): parse_value(
                f"{subkey}.value", subvalue, subvalue_type
            )
            for subkey, subvalue in value.items()
        }

    if origin is Union:
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
    if value_type is Any:
        return value
    if value is None and value_type is not NoneType:
        raise KeyError(f"`{name}` of type `{value_type}` is required.")

    if issubclass(value_type, Enum):
        return value_type(value)
    if issubclass(value_type, datetime):
        return parse_utc_timestamp(value)
    if value_type is float and isinstance(value, int):
        return float(value)
    if value_type is int and isinstance(value, str) and value.isnumeric():
        return int(value)
    if not isinstance(value, value_type):
        raise TypeError(
            f"Value {value} of type {type(value)} is invalid for {name}, "
            f"expected value of type {value_type}"
        )
    return value


def dataclass_from_dict(cls: dataclass, dict_obj: dict, strict=False):
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

    return cls(
        **{
            field.name: parse_value(
                f"{cls.__name__}.{field.name}",
                dict_obj.get(field.name),
                field.type,
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
            return "0.0.0"
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
