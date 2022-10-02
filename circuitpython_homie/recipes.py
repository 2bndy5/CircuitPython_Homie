"""The :mod:`circuitpython_homie.recipes` module holds any suggested recipes for easily
implementing common node properties.

.. important::
    Callback methods are not templated for these properties. Users are advised to
    write their own callback methods and set them to the desired property's
    :attr:`~circuitpython_homie.HomieProperty.callback` attribute.

.. |param_mutable| replace:: (can be overridden with a keyword argument)
.. |param_immutable| replace:: (shall not be overridden)
.. |param_intro| replace:: The parameters here follow the `HomieProperty` constructor
    signature, but with a few exceptions:
.. _ISO 8601: https://en.wikipedia.org/wiki/ISO_8601
.. _ISO 8601 Duration: https://en.wikipedia.org/wiki/ISO_8601#Durations
"""
import time

try:
    from typing import Sequence, List, Union
except ImportError:  # pragma: no cover
    pass  # do not type check on CircuitPython firmware

from . import HomieProperty


class _PropertyColor(HomieProperty):
    def __init__(self, name: str, property_id: str = None, **extra_attributes):
        extra_attributes.pop("datatype", None)
        super().__init__(
            name,
            "color",
            property_id=property_id,
            init_value=self.validate(extra_attributes.pop("init_value", "0,0,0")),
            **extra_attributes,
        )

    def validate(self, color: Union[str, Sequence[int]]) -> List[int]:
        """Translate a color string into a valid 3-tuple of integers.

        :param color: The color as a string in which the elements are delimited by
            commas (``,``).
        :throws: An `AssertionError` is raised when the given color string is malformed
            or the color's components are out of bounds.
        :returns: A 3 `tuple` consisting of the color's 3 components.
        """
        if isinstance(color, str):
            elements = [int(x) for x in color.split(",")]
        else:
            elements = list(color)
        assert len(elements) == 3, "expected 3 color components, got {}".format(
            len(elements)
        )
        return elements

    def _set(self, value: Union[str, Sequence[int]]) -> List[int]:
        return super()._set(self.validate(value))


class PropertyRGB(_PropertyColor):
    """A property that can be used to represent node's color in RGB format.

    |param_intro|

    - ``settable`` attribute is set to `True` |param_mutable|
    - ``init_value`` is set to black :python:`"0,0,0"` |param_mutable|
    - `datatype` attribute is set to :python:`"color"` |param_immutable|
    - ``format`` attribute is set to :python:`"rgb"` |param_immutable|
    """

    def __init__(self, name: str, property_id: str = None, **extra_attributes):
        extra_attributes.pop("format", None)
        super().__init__(
            name,
            property_id=property_id,
            format="rgb",
            **extra_attributes,
        )

    def validate(self, color: Union[str, Sequence[int]]) -> List[int]:
        elements = super().validate(color)
        for elem in elements:
            assert 0 <= elem <= 255, "{} is not in range [0, 255]".format(elem)
        return elements


class PropertyHSV(_PropertyColor):
    """A property that can be used to represent node's color in HSV format.

    |param_intro|

    - ``init_value`` is set to black :python:`"0,0,0"` |param_mutable|
    - `datatype` attribute is set to :python:`"color"` |param_immutable|
    - ``format`` attribute is set to :python:`"hsv"` |param_immutable|
    """

    def __init__(self, name: str, property_id: str = None, **extra_attributes):
        super().__init__(
            name,
            property_id=property_id,
            format=extra_attributes.pop("format", "hsv"),
            **extra_attributes,
        )

    def validate(self, color: Union[str, Sequence[int]]) -> List[int]:
        elements = super().validate(color)
        for i, elem in enumerate(elements):
            if not i:
                assert 0 <= elem <= 360, "{} is not a valid Hue value".format(elem)
            else:
                assert 0 <= elem <= 100, "{} is not in range [0, 100]".format(elem)
        return elements


class PropertyDateTime(HomieProperty):
    """A property that represents a data and time in `ISO 8601`_ format.

    |param_intro|

    - `datatype` attribute is set to :python:`"datetime"` |param_immutable|
    - ``init_value`` is set to :python:`"2000-01-01T00:00:00"` |param_mutable|

    .. hint::
        Validation of the payload format can be done using the `datetime` library
        or the `adafruit_datetime` library.
    """

    def __init__(
        self,
        name: str,
        property_id: str = None,
        init_value="2000-01-01T00:00:00",
        **extra_attributes
    ):
        extra_attributes.pop("datatype", None)
        super().__init__(name, "datetime", property_id, init_value, **extra_attributes)

    @staticmethod
    def convert(value: time.struct_time) -> str:
        """Takes a :class:`~time.struct_time` object and returns a `str` in compliance
        with `ISO 8601`_ standards.

        :param value: The `named tuple` to translate.
        :returns: A `ISO 8601`_ compliant formatted string in the form
            ``YYYY-MM-DDTHH:MM:SS``.
        """
        return "{:04}-{:02}-{:02}T{:02}:{:02}:{:02}".format(
            value.tm_year,
            value.tm_mon,
            value.tm_mday,
            value.tm_hour,
            value.tm_min,
            value.tm_sec,
        )

    def _set(self, value: Union[str, time.struct_time]) -> str:
        """Set the property's value.

        :param value: This parameter can be:

            - A `str` in `ISO 8601`_ format. To validate the format of this string, use
              the `datetime` library or the `adafruit_datetime` library.
            - A `time.struct_time` object which will be converted to `ISO 8601`_
              datetime format (via `convert()`).
        :returns: The `str` form of the given value.
        """
        if isinstance(value, time.struct_time):
            return super()._set(self.convert(value))
        assert value, "a payload representing time cannot be an empty string."
        return super()._set(value)


class PropertyDuration(HomieProperty):
    """A property that represents a duration of time in `ISO 8601 Duration`_ format.

    |param_intro|

    - `datatype` attribute is set to :python:`"duration"` |param_immutable|
    - ``init_value`` is set to :python:`"PT0S"` |param_mutable|

    .. hint::
        Validation of the payload format can be done using the `datetime` library
        or the `adafruit_datetime` library.
    """

    def __init__(
        self, name: str, property_id: str = None, init_value="PT0S", **extra_attributes
    ):
        extra_attributes.pop("datatype", None)
        super().__init__(name, "duration", property_id, init_value, **extra_attributes)

    @staticmethod
    def convert(value: Union[int, float]) -> str:
        """Takes a a number of seconds and returns a `str` in compliance
        with `ISO 8601 Duration`_ standards.

        .. note:: For minimality, this function will only convert a number of seconds
            into units of hours, minutes, and seconds.

        :param value: The number of seconds that describe a duration. If a `float`
            object is passed, then the fractional seconds are truncated.
        :returns: A `ISO 8601 Duration`_ compliant formatted string in the form
            ``PTnHnMnS``.

            Only  units with a non-zero value are represented. For instance, a value of
            :python:`59` will return :python:`"PT59S"` (representing 59 seconds), and a
            value of :python:`3609` will return :python:`"PT1H9S"` (representing 1 hour
            and 9 seconds).
        """
        if isinstance(value, float):
            value = int(value)
        second = value % 60
        minute = int((value % 3600) / 60)
        hour = int(value / 3600)
        time_duration = "PT"
        if hour:
            time_duration += "{}H".format(hour)
        if minute:
            time_duration += "{}M".format(minute)
        if second or (not hour and not minute):
            time_duration += "{}S".format(second)
        return time_duration

    def _set(self, value: Union[str, int]) -> str:
        """Set the property's value.

        :param value: This parameter can be:

            - A `str` in `ISO 8601`_ format. To validate the format of this string, use
              the `datetime` library or the `adafruit_datetime` library.
            - An `int` number of seconds which will be converted to `ISO 8601`_
              duration format (via `convert()`).
        :returns: The `str` form of the given value.
        """
        if isinstance(value, (int, float)):
            return super()._set(self.convert(value))
        assert value, "a payload representing time cannot be an empty string."
        return super()._set(value)


class PropertyBool(HomieProperty):
    """A property to represent boolean data.

    |param_intro|

    - `datatype` attribute is set to :python:`"boolean"` |param_immutable|
    - ``init_value`` is set to `False` |param_mutable|
    """

    def __init__(
        self, name: str, property_id: str = None, init_value=False, **extra_attributes
    ):
        extra_attributes.pop("datatype", None)
        super().__init__(
            name, "boolean", property_id, self.validate(init_value), **extra_attributes
        )

    @staticmethod
    def validate(value: Union[str, bool]) -> bool:
        """Validates a `str` that describes a boolean.

        :param value: The boolean's description. According to the Homie specifications,
            this string value can only be :python:`"true` or :python:`"false"`
            (case-sensitive).

            This function will convert the given `str` to lowercase form. If a `bool`
            is passed, then this function simply returns it.
        :returns: A `bool` object.
        :throws: An `AssertionError` is raised if the given string value is not in
            compliance with Homie specifications.
        """
        if isinstance(value, bool):
            return value
        value = value.lower()
        assert value in (
            "true",
            "false",
        ), "{} is not a valid boolean description".format(value)
        return value == "true"

    def _set(self, value: Union[bool, str]) -> bool:
        return super()._set(self.validate(value))


class _PropertyNumber(HomieProperty):
    def __init__(
        self,
        name: str,
        datatype: str,
        property_id: str = None,
        init_value=0,
        **extra_attributes
    ):
        assert datatype in ("integer", "float")
        self.datatype = datatype  # needs to be set for using validate()
        if "format" in extra_attributes:
            setattr(self, "format", extra_attributes["format"])
        super().__init__(
            name, datatype, property_id, self.validate(init_value), **extra_attributes
        )

    def validate(self, value: Union[str, int, float]) -> Union[int, float]:
        """Make assertions that a given value is in the ``format`` range.

        :param value: The value to validate. If this value is a `str`, then it is
            converted to an `int` or `float` according to the `datatype` attribute.
        :throws: An `AssertionError` is raised when the given ``value`` is malformed.
        :returns: The validated value (as specified by the ``value`` parameter).
        """
        is_float = self.datatype == "float"
        if isinstance(value, str):
            value = int(value) if not is_float else float(value)
        if hasattr(self, "format"):
            fmt = getattr(self, "format").split(":")  # type: List[str]
            assert len(fmt) == 2, "expected `<min>:<max>` form, got {}.".format(value)
            low = int(fmt[0]) if not is_float else float(fmt[0])
            high = int(fmt[1]) if not is_float else float(fmt[1])
            if low > high:
                low, high = (high, low)
            assert low <= value <= high, "{} is not in range of [{}, {}]".format(
                value, low, high
            )
        return value

    def _set(self, value: Union[str, int, float]) -> Union[int, float]:
        return super()._set(self.validate(value))


class PropertyPercent(_PropertyNumber):
    """A property that represents a percentage.

    The parameters here follow the `HomieProperty` constructor signature, but with
    a few exceptions:

    - ``unit`` attribute is set to :python:`"%"` |param_immutable|
    - `datatype` attribute is constrained to :python:`"integer"` or its default
      :python:`"float"` values |param_mutable|
    - ``format`` attribute is set to :python:`"0:100"`, which describes an inclusive
      range from 0 to 100, but it is not have to be this range |param_mutable|
    - ``init_value`` defaults to :python:`0` because percentage type payloads cannot be
      empty rings |param_mutable|
    """

    def __init__(
        self,
        name: str,
        datatype: str = "float",
        property_id: str = None,
        init_value=0,
        **extra_attributes
    ):
        extra_attributes.pop("unit", None)
        super().__init__(
            name,
            datatype,
            property_id,
            init_value,
            format=extra_attributes.pop("format", "0:100"),
            unit="%",
            **extra_attributes,
        )


class PropertyInt(_PropertyNumber):
    """A property to represent an integer.

    |param_intro|

    - `datatype` attribute is set to :python:`"integer"` |param_immutable|
    - ``init_value`` is set to :python:`0` |param_mutable|
    - ``format`` attribute can optionally be used to define the constraining
      range. By default, the ``format`` attribute is unspecified |param_mutable|.
    """

    def __init__(
        self, name: str, property_id: str = None, init_value=0, **extra_attributes
    ):
        extra_attributes.pop("datatype", None)
        super().__init__(name, "integer", property_id, init_value, **extra_attributes)


class PropertyFloat(_PropertyNumber):
    """A property to represent an float.

    |param_intro|

    - `datatype` attribute is set to :python:`"float"` |param_immutable|
    - ``init_value`` is set to :python:`0.0` |param_mutable|
    - ``format`` attribute can optionally be used to define the constraining
      range. By default, the ``format`` attribute is unspecified |param_mutable|.
    """

    def __init__(
        self, name: str, property_id: str = None, init_value=0.0, **extra_attributes
    ):
        extra_attributes.pop("datatype", None)
        super().__init__(name, "float", property_id, init_value, **extra_attributes)


class PropertyEnum(HomieProperty):
    """A property that represent an option amongst a defined list of valid options.

    |param_intro|
    - `datatype` attribute is set to :python:`"enum"` |param_immutable|
    - ``format`` attribute is required and must be a `list` or `tuple`.
    - ``init_value`` will be the first item in ``format`` |param_mutable|
    """

    def __init__(
        self,
        name: str,
        format: Union[list, tuple],  # pylint: disable=redefined-builtin
        property_id: str = None,
        init_value="",
        **extra_attributes
    ):
        extra_attributes.pop("datatype", None)
        if not isinstance(format, (list, tuple)):
            raise ValueError("`format` shall be a list or tuple of values.")
        assert format, "`format` cannot be an empty sequence."
        if not init_value:
            init_value = format[0]
        else:
            assert init_value in format, "init_value is not in {}".format(format)
        super().__init__(
            name, "enum", property_id, init_value, format=format, **extra_attributes
        )

    def validate(self, value: Union[str, int, float]):
        """Ensure that the given ``value`` is part of the defined ``format`` attribute.

        :param value: The specified value. This `type` should correspond to the `type`
            used in the defined ``format``.
        :returns: The valid value.
        :throws:
            - An `AssertionError` if the given value is not in the defined ``format``.
        """
        fmt = getattr(self, "format")  # type: Union[List, tuple]
        assert value in fmt, "{} is not in {}".format(value, fmt)
        return value

    def _set(self, value):
        return super()._set(self.validate(value))
