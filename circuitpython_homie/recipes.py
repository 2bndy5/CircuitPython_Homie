"""The ``recipes`` module holds any suggested recipes for easily implementing common
node properties.

.. important::
    Callback methods are not templated for these properties. Users are advised to
    write their own callback methods and set them to the desired property's
    :attr:`~circuitpython_homie.HomieProperty.callback` attribute.

.. |param_mutable| replace:: (can be overridden with a keyword argument)
.. |param_immutable| replace:: (cannot be overridden)
.. |param_intro| replace:: The parameters here follow the `HomieProperty` constructor
    signature, but with a few exceptions:
.. _ISO 8601: https://en.wikipedia.org/wiki/ISO_8601
"""
import time

try:
    from typing import Tuple, List, Union
except ImportError:
    pass  # do not type check on CircuitPython firmware

from . import HomieProperty


class _PropertyColor(HomieProperty):
    def __init__(self, name: str, property_id: str = None, **extra_attributes):
        extra_attributes.pop("datatype", None)
        super().__init__(
            name,
            "color",
            property_id=property_id,
            init_value=extra_attributes.pop("init_value", "0,0,0"),
            settable=extra_attributes.pop("settable", True),
            **extra_attributes,
        )

    def validate(self, color: str) -> Tuple[int, int, int]:
        """Translate a color string into a valid 3-tuple of integers.

        :param color: The color as a string in which the elements are delimited by
            commas (``,``).
        :throws: An `AssertionError` is raised when the given color string is malformed.
        :returns: A 3 `tuple` consisting of the color's 3 components.
        """
        elements = color.split(",")
        assert len(elements) == 3, "expected 3 color elements, got {}".format(
            len(elements)
        )
        for elem in elements:
            assert elem.isdigit()
        return tuple(int(x) for x in elements)

    def set(self, value: str) -> Tuple[int, int, int]:
        return self.validate(super().set(value))


class PropertyRGB(_PropertyColor):
    """A property that can be used to represent node's color in RGB format.

    |param_intro|

    - ``settable`` attribute is set to `True` |param_mutable|
    - ``init_value`` is set to black ``"0,0,0"`` |param_mutable|
    - ``datatype`` attribute is set to ``"color"`` |param_immutable|
    - ``format`` attribute is set to ``"rgb"`` |param_immutable|
    """

    def __init__(self, name: str, property_id: str = None, **extra_attributes):
        extra_attributes.pop("format", None)
        super().__init__(
            name,
            property_id=property_id,
            format="rgb",
            **extra_attributes,
        )

    def validate(self, color: str) -> Tuple[int, int, int]:
        elements = super().validate(color)
        for elem in elements:
            assert 0 <= elem <= 255, "{} is not in range [0, 255]".format(elem)
        return elements


class PropertyHSV(_PropertyColor):
    """A property that can be used to represent node's color in HSV format.

    |param_intro|

    - ``settable`` attribute is set to `True` |param_mutable|
    - ``init_value`` is set to black ``"0,0,0"`` |param_mutable|
    - ``datatype`` attribute is set to ``"color"`` |param_immutable|
    - ``format`` attribute is set to ``"hsv"`` |param_immutable|
    """

    def __init__(self, name: str, property_id: str = None, **extra_attributes):
        super().__init__(
            name,
            property_id=property_id,
            format=extra_attributes.pop("format", "hsv"),
            **extra_attributes,
        )

    def validate(self, color: str) -> Tuple[int, int, int]:
        elements = super().validate(color)
        for i, elem in enumerate(elements):
            if not i:
                assert 0 <= elem <= 360, "{} is not a valid Hue value".format(elem)
            else:
                assert 0 <= elem <= 100, "{} is not in range [0, 100]".format(elem)
        return elements


class PropertyPercent(HomieProperty):
    """A property that represents a percentage.

    The parameters here follow the `HomieProperty` constructor signature, but with
    a few exceptions:

    - ``unit`` attribute is set to ``"%"`` |param_immutable|
    - ``datatype`` attribute is constrained to ``"integer"`` or  its default
      ``"float"`` values |param_mutable|
    - ``format`` attribute is set to ``"0:100"``, which describes a range from 0 to
      100, but are not limited to this range |param_mutable|
    - ``init_value`` defaults to ``0`` because percentage type payloads cannot be empty
      strings |param_mutable|
    """

    def __init__(
        self,
        name: str,
        datatype: str = "float",
        property_id: str = None,
        init_value=0,
        **extra_attributes
    ):
        assert datatype in ("integer", "float")
        super().__init__(
            name,
            datatype,
            property_id,
            init_value,
            format=extra_attributes.pop("format", "0:100"),
            **extra_attributes,
        )

    def validate(self, value: Union[int, float]) -> Union[int, float]:
        """Make assertions that a given value is in the ``format`` range.

        :param value: The value to validate.
        :throws: An `AssertionError` is raised when the given ``value`` is malformed.
        :returns: The validated value (as specified by the ``value`` parameter).
        """
        fmt = getattr(self, "format").split(":")  # type: List[str]
        assert len(fmt) == 2, "expected `<min>:<max>` form, got {}.".format(value)
        low, high = tuple(int(x) for x in fmt)
        if self.datatype == "float":
            low, high = tuple(float(x) for x in fmt)
        assert low <= value <= high, "{} is not in range of [{}, {}]".format(
            value, low, high
        )
        return value

    def set(self, value: Union[int, float]) -> Union[int, float]:
        return self.validate(super().set(value))


class PropertyDateTime(HomieProperty):
    """A property that represents a data and time in `ISO 8601`_ format.

    |param_intro|

    - ``datatype`` attribute is set to ``"datetime"`` |param_immutable|
    - ``init_value`` is set to ``"2000-01-01T00:00:00"`` |param_mutable|

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

    def set(self, value: Union[str, time.struct_time]) -> str:
        """Set the property's value.

        :param value: This parameter can be:

            - A `str` in `ISO 8601`_ format. To validate the format of this string, use
              the `datetime` library or the `adafruit_datetime` library.
            - A `time.struct_time` object which will be converted to `ISO 8601`_
              datetime format (via `convert()`).
        :returns: The `str` form of the given value.
        """
        if isinstance(value, time.struct_time):
            return super().set(self.convert(value))
        return super().set(value)


class PropertyBool(HomieProperty):
    """A property to represent boolean data.

    |param_intro|

    - ``datatype`` attribute is set to ``"boolean"`` |param_immutable|
    - ``settable`` attribute is set to `True` |param_mutable|
    - ``init_value`` is set to ``"false"`` |param_mutable|
    """

    def __init__(
        self, name: str, property_id: str = None, init_value="false", **extra_attributes
    ):
        extra_attributes.pop("datatype", None)
        super().__init__(
            name,
            "boolean",
            property_id,
            init_value,
            settable=extra_attributes.pop("settable", True),
            **extra_attributes,
        )

    @staticmethod
    def validate(value: Union[str, bool]) -> bool:
        """Validates a `str` that describes a boolean.

        :param value: The boolean's description. According to the Homie specifications,
            this string value can only be ``"true`` or ``"false"`` (case-sensitive).

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

    def set(self, value: Union[bool, str]) -> bool:
        actual_value = self.validate(value)
        super().set("true" if actual_value else "false")
        return actual_value
