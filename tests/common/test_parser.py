"""Test parser functions that converts the incoming json from API into dataclass models."""
import datetime
from dataclasses import dataclass
from typing import Optional

import pytest

from matter_server.common.helpers.util import dataclass_from_dict


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
    g: str = "default"


def test_dataclass_from_dict():
    """Test dataclass from dict parsing."""
    raw = {
        "a": 1,
        "b": 1.0,
        "c": "hello",
        "d": 1,
        "e": {"a": 2, "b": "test", "c": "test", "d": None},
        "f": "2022-12-09T06:58:00Z",
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
    assert res.g == "default"
    # test int gets converted to float
    raw["b"] = 2
    res = dataclass_from_dict(BasicModel, raw)
    assert res.b == 2.0
    # test datetime string
    assert isinstance(res.f, datetime.datetime)
    assert res.f.month == 12
    assert res.f.day == 9
    # test string doesn't match int
    with pytest.raises(TypeError):
        raw2 = {**raw}
        raw2["a"] = "blah"
        dataclass_from_dict(BasicModel, raw2)
    # test missing key result in keyerror
    with pytest.raises(KeyError):
        raw2 = {**raw}
        del raw2["a"]
        dataclass_from_dict(BasicModel, raw2)
    # test extra keys silently ignored in non-strict mode
    raw2 = {**raw}
    raw2["extrakey"] = "something"
    dataclass_from_dict(BasicModel, raw2, strict=False)
    # test extra keys not silently ignored in strict mode
    with pytest.raises(KeyError):
        dataclass_from_dict(BasicModel, raw2, strict=True)
