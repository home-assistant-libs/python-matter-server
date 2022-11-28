"""Utils for Matter server (and client)."""
from base64 import b64encode
from dataclasses import MISSING, asdict, dataclass, fields, is_dataclass
from datetime import date, datetime
from enum import Enum
from functools import cache
from importlib.metadata import PackageNotFoundError, version as pkg_version
import logging
import platform
from typing import Any, Dict, Optional, Set, Type, Union, get_args, get_origin

from chip.clusters import Cluster, ClusterObject
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

# TODO: The below dataclass utils are shamelessly copied from aiohue
# we should abstract these into a seperate helper library some day
# https://github.com/home-assistant-libs/aiohue/blob/master/aiohue/util.py


def update_dataclass(cur_obj: dataclass, new_vals: dict) -> Set[str]:
    """
    Update instance of dataclass from (partial) dict.

    Returns: Set with changed keys.
    """
    changed_keys = set()
    for f in fields(cur_obj):
        cur_val = getattr(cur_obj, f.name, None)
        new_val = new_vals.get(f.name)

        # handle case where value is sub dataclass/model
        if is_dataclass(cur_val) and isinstance(new_val, dict):
            for subkey in update_dataclass(cur_val, new_val):
                changed_keys.add(f"{f.name}.{subkey}")
            continue
        # parse value from type annotations
        new_val = parse_value(f.name, new_val, f.type, cur_val)
        if cur_val == new_val:
            continue
        setattr(cur_obj, f.name, new_val)
        changed_keys.add(f.name)
    return changed_keys


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


def parse_value(name: str, value: Any, value_type: Type, default: Any = MISSING):
    """Try to parse a value from raw (json) data and type definitions."""

    if isinstance(value_type, str):
        value_type = eval(value_type)

    # if issubclass(value_type, Cluster):
    #     return Cluster.FromDict(value)

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