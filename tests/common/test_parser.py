"""Test parser functions that converts the incoming json from API into dataclass models."""

from dataclasses import dataclass
import datetime
from enum import Enum, IntEnum
from typing import Optional, Union

from chip.clusters.Types import Nullable, NullValue
import pytest

from matter_server.common.helpers.util import dataclass_from_dict, parse_value


class MatterIntEnum(IntEnum):
    """Basic Matter Test IntEnum"""

    A = 0
    B = 1
    C = 2


class MatterEnum(Enum):
    """Basic Matter Test Enum"""

    A = "a"
    B = "b"
    C = "c"


@dataclass
class BasicModelChild:
    """Basic test model."""

    a: int
    b: str
    c: str
    d: Optional[int]


@dataclass
class BasicModel:
    """Basic test model."""

    a: int
    b: float
    c: str
    d: Optional[int]
    e: BasicModelChild
    f: datetime.datetime
    g: MatterEnum
    h: MatterIntEnum
    i: str = "default"


def test_dataclass_from_dict():
    """Test dataclass from dict parsing."""
    raw = {
        "a": 1,
        "b": 1.0,
        "c": "hello",
        "d": 1,
        "e": {"a": 2, "b": "test", "c": "test", "d": None},
        "f": "2022-12-09T06:58:00Z",
        "g": "a",
        "h": 2,
    }
    res = dataclass_from_dict(BasicModel, raw)
    # test the basic values
    assert isinstance(res, BasicModel)
    assert res.a == 1
    assert res.b == 1.0
    assert res.d == 1
    # test recursive parsing
    assert isinstance(res.e, BasicModelChild)
    # test default value
    assert res.i == "default"
    # test int gets converted to float
    raw["b"] = 2
    res = dataclass_from_dict(BasicModel, raw)
    assert res.b == 2.0
    # test datetime string
    assert isinstance(res.f, datetime.datetime)
    assert res.f.month == 12
    assert res.f.day == 9
    # test parse (valid) MatterEnum
    assert res.g == MatterEnum.A
    # test parse (valid) MatterIntEnum
    assert res.h == MatterIntEnum.C
    # test parse invalid enum value returns raw value
    raw2 = {**raw}
    raw2["h"] = 5
    res2 = dataclass_from_dict(BasicModel, raw2)
    assert res2.h == 5
    # test string doesn't match int
    with pytest.raises(TypeError):
        raw2 = {**raw}
        raw2["a"] = "blah"
        dataclass_from_dict(BasicModel, raw2)
    # test missing key result in keyerror
    with pytest.raises(KeyError):
        raw2 = {**raw}
        del raw2["a"]
        dataclass_from_dict(BasicModel, raw2, strict=True)
    # test extra keys silently ignored in non-strict mode
    raw2 = {**raw}
    raw2["extrakey"] = "something"
    dataclass_from_dict(BasicModel, raw2, strict=False)
    # test extra keys not silently ignored in strict mode
    with pytest.raises(KeyError):
        dataclass_from_dict(BasicModel, raw2, strict=True)
    # test NOCStruct.noc edge case
    res = parse_value("NOCStruct.noc", 5, bytes)
    assert res == b""


def test_parse_value():
    """Test special cases in the parse_value helper."""
    # test None value which is allowed
    assert parse_value("test", None, int, allow_none=True) is None
    # test unexpected None value
    with pytest.raises(KeyError):
        parse_value("test", None, int, allow_none=False)
    # test sdk Nullable type
    assert parse_value("test", None, Nullable) is None
    assert parse_value("test", None, Nullable, allow_sdk_types=True) == NullValue
    assert (
        parse_value(
            "test", None, Union[int, Nullable], allow_none=False, allow_sdk_types=True
        )
        == NullValue
    )
