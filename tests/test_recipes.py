"""Test validation and conversion of specific types of properties' values."""
import time
from typing import List, Tuple, Union, Optional
import pytest
from circuitpython_homie.recipes import (
    PropertyRGB,
    PropertyHSV,
    PropertyBool,
    PropertyInt,
    PropertyFloat,
    PropertyPercent,
    PropertyDateTime,
    PropertyDuration,
    PropertyEnum,
)

# pylint: disable=protected-access


@pytest.mark.parametrize(
    "color,expected",
    [
        ("255,127,0", (255, 127, 0)),
        ((255, 127, 0), (255, 127, 0)),
        pytest.param("355,0,0", (0, 0, 0), marks=pytest.mark.xfail),
        pytest.param("-1,0,0", (0, 0, 0), marks=pytest.mark.xfail),
    ],
)
def test_rgb(color: str, expected: Tuple[int, int, int]):
    """Test RGB color property validation."""
    rgb = PropertyRGB("color", init_value=color)
    result = list(expected)
    assert rgb.value == result
    assert rgb._set(color) == result


@pytest.mark.parametrize(
    "color,expected",
    [
        ("255,85,0", (255, 85, 0)),
        ((255, 85, 0), (255, 85, 0)),
        pytest.param("720,0,0", (0, 0, 0), marks=pytest.mark.xfail),
        pytest.param("0,-1,0", (0, 0, 0), marks=pytest.mark.xfail),
    ],
)
def test_hsv(color: str, expected: Tuple[int, int, int]):
    """Test HSV color property validation."""
    hsv = PropertyHSV("color", init_value=color)
    result = list(expected)
    assert hsv.value == result
    assert hsv._set(color) == result


@pytest.mark.parametrize(
    "value,expected",
    [
        ("true", True),
        ("false", False),
        (True, True),
        pytest.param("0", False, marks=pytest.mark.xfail),
    ],
)
def test_bool(value: str, expected: bool):
    """Test boolean property validation."""
    prop = PropertyBool("switch", init_value=value)
    assert prop.value is expected
    assert prop._set(not expected) is not expected


@pytest.mark.parametrize("value", [0, 1, 50, "42"])
@pytest.mark.parametrize("format_range", [None, "0:60", "50:-1"])
def test_int(value: int, format_range: str):
    """Test integer property validation."""
    args = dict(init_value=value)
    if format_range:
        args["format"] = format_range
    prop = PropertyInt("number", **args)
    result = int(value)
    assert prop.value == result
    assert prop._set(value) == result


@pytest.mark.parametrize("value", [0, 1.5, 45.6, "42"])
@pytest.mark.parametrize("format_range", [None, "0:60", "50:-1"])
def test_float(value: float, format_range: str):
    """Test float property validation."""
    args = dict(init_value=value)
    if format_range:
        args["format"] = format_range
    prop = PropertyFloat("number", **args)
    result = float(value)
    assert prop.value == result
    assert prop._set(value) == result


@pytest.mark.parametrize(
    "value,datatype",
    [
        (0, "integer"),
        (1, "integer"),
        (1.5, "float"),
        (45.6, "float"),
        ("42.5", "float"),
        ("42", "integer"),
    ],
)
@pytest.mark.parametrize("format_range", [None, "0:60", "50:-1"])
def test_percent(value: Union[int, float], datatype: str, format_range: str):
    """Test percentage property validation."""
    args = dict(datatype=datatype, init_value=value)
    if format_range:
        args["format"] = format_range
    prop = PropertyPercent("number", **args)
    assert hasattr(prop, "unit") and getattr(prop, "unit") == "%"
    assert getattr(prop, "datatype") == datatype
    if isinstance(value, str):
        if getattr(prop, "datatype") == "float":
            result = float(value)
        else:
            result = int(value)
    else:
        result = value
    assert prop.value == result
    assert prop._set(value) == result


@pytest.mark.parametrize(
    "value,expected",
    [
        ("invalid-time", "invalid-time"),
        (time.struct_time((0, 1, 1, 0, 0, 0, 0, 1, 0)), "0000-01-01T00:00:00"),
    ],
)
def test_datetime(value: Union[str, time.struct_time], expected: str):
    """Test conversion of DateTime property."""
    prop = PropertyDateTime("time")
    assert prop.datatype == "datetime"
    assert prop.value == "2000-01-01T00:00:00"
    assert prop._set(value) == expected


@pytest.mark.parametrize(
    "value,expected",
    [
        ("invalid-time", "invalid-time"),
        (59, "PT59S"),
        (3609, "PT1H9S"),
        (360, "PT6M"),
        (0.5, "PT0S"),
    ],
)
def test_duration(value: Union[str, int], expected: str):
    """Test conversion of Duration property."""
    prop = PropertyDuration("time")
    assert prop.datatype == "duration"
    assert prop.value == "PT0S"
    assert prop._set(value) == expected


@pytest.mark.parametrize(
    "value", ["0", 1, 2.5, pytest.param(9, marks=pytest.mark.xfail)]
)
@pytest.mark.parametrize(
    "enum",
    [("0", 1, 2.5, 5), ["0", 1, 2.5, 5], pytest.param(None, marks=pytest.mark.xfail)],
)
@pytest.mark.parametrize("init", [None, 5, pytest.param(9, marks=pytest.mark.xfail)])
def test_enum(
    value: Union[str, int, float],
    enum: Optional[Union[List[Union[str, int, float]], Tuple[str, int, float]]],
    init: Optional[Union[str, int, float]],
):
    """Test validation of an enumerator in an enumerated property."""
    if init is not None:
        prop = PropertyEnum("enumeration", enum, init_value=init)
    else:
        prop = PropertyEnum("enumeration", enum)
    assert prop.datatype == "enum"

    assert prop._set(value) == value
