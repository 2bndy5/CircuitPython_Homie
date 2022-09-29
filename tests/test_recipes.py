"""Test validation and conversion of specific types of properties' values."""
import time
from typing import List, Tuple, Union
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


@pytest.mark.parametrize(
    "color,expected",
    [
        ("255,127,0", (255, 127, 0)),
        pytest.param("355,0,0", (0, 0, 0), marks=pytest.mark.xfail),
        pytest.param("-1,0,0", (0, 0, 0), marks=pytest.mark.xfail),
    ],
)
def test_rgb(color: str, expected: Tuple[int, int, int]):
    """Test RGB color property validation."""
    rgb = PropertyRGB("color")
    assert rgb.set(color) == expected


@pytest.mark.parametrize(
    "color,expected",
    [
        ("255,85,0", (255, 85, 0)),
        pytest.param("720,0,0", (0, 0, 0), marks=pytest.mark.xfail),
        pytest.param("0,-1,0", (0, 0, 0), marks=pytest.mark.xfail),
    ],
)
def test_hsv(color: str, expected: Tuple[int, int, int]):
    """Test HSV color property validation."""
    hsv = PropertyHSV("color")
    assert hsv.set(color) == expected


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
    prop = PropertyBool("switch")
    assert prop.set(value) is expected


@pytest.mark.parametrize("value", [0, 1, 50, "42"])
@pytest.mark.parametrize("format_range", [None, "0:60", "50:-1"])
def test_int(value: int, format_range: str):
    """Test integer property validation."""
    prop = PropertyInt("number")
    if format_range:
        setattr(prop, "format", format_range)
    assert prop.set(value) is (value if isinstance(value, int) else int(value))


@pytest.mark.parametrize("value", [0, 1.5, 45.6, "42"])
@pytest.mark.parametrize("format_range", [None, "0:60", "50:-1"])
def test_float(value: float, format_range: str):
    """Test float property validation."""
    prop = PropertyFloat("number")
    if format_range:
        setattr(prop, "format", format_range)
    assert prop.set(value) == (value if isinstance(value, float) else float(value))


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
    prop = PropertyPercent("number", datatype=datatype)
    assert hasattr(prop, "unit") and getattr(prop, "unit") == "%"
    assert getattr(prop, "datatype") == datatype
    if format_range:
        setattr(prop, "format", format_range)
    if isinstance(value, str):
        if getattr(prop, "datatype") == "float":
            assert prop.set(value) == float(value)
        else:
            assert prop.set(value) == int(value)
    else:
        assert prop.set(value) == value


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
    assert prop() == "2000-01-01T00:00:00"
    assert prop.set(value) == expected


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
    assert prop() == "PT0S"
    assert prop.set(value) == expected


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
    enum: Union[List[Union[str, int, float]], Tuple[str, int, float]],
    init,
):
    """Test validation of an enumerator in an enumerated property."""
    if init:
        prop = PropertyEnum("enumeration", enum, init_value=init)
    else:
        prop = PropertyEnum("enumeration", enum)
    assert prop.datatype == "enum"
    prop.set(value)  # assertions are done internally
