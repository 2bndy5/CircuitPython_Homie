# SPDX-FileCopyrightText: Copyright (c) 2022 Brendan Doherty
#
# SPDX-License-Identifier: MIT
"""
This module holds the Homie implementation for a device.
See the nodes.py and properties.py for other Homie implementations.
"""
try:
    from os import uname
except ImportError:
    from platform import uname

try:
    from typing import List, Dict, Any
except ImportError:
    pass  # don't type check on CircuitPython firmware

import re
from adafruit_minimqtt.adafruit_minimqtt import MQTT, MMQTTException

__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/2bndy5/CircuitPython_Homie.git"

DEVICE_STATES = [
    "init",
    "ready",
    "disconnected",
    "sleeping",
    "alert",
    "lost",
]
"""A list of valid device states according to the
`Homie specification's Life Cycle
<https://homieiot.github.io/specification/#device-lifecycle>`_."""

PAYLOAD_TYPES = [
    "integer",
    "float",
    "boolean",
    "string",
    "enum",
    "color",
    "datetime",
    "duration",
]
"""A valid payload type (per Homie specifications) is one of these defined types:

- `integer <https://homieiot.github.io/specification/spec-core-v4_0_0/#integer>`_
- `float <https://homieiot.github.io/specification/spec-core-v4_0_0/#float>`_
- `boolean <https://homieiot.github.io/specification/spec-core-v4_0_0/#boolean>`_
- `string <https://homieiot.github.io/specification/spec-core-v4_0_0/#string>`_
- `enum <https://homieiot.github.io/specification/spec-core-v4_0_0/#enum>`_
- `color <https://homieiot.github.io/specification/spec-core-v4_0_0/#color>`_
- `datetime <https://homieiot.github.io/specification/spec-core-v4_0_0/#datetime>`_
- `duration <https://homieiot.github.io/specification/spec-core-v4_0_0/#duration>`_
"""


def validate_id(_id: str) -> str:
    """Conform and validate a given ID to Homie specifications.

    :param _id: The given ID.

        .. note::
            This function strips ``-`` characters from the beginning and ending
            of the ID. A leading ``$`` is also removed since that character is
            reserved for Homie attributes.
    :throws: If the given ID contains anything other than
        lowercase letters (a-z), numbers (0-9), or hyphens (``-``), then
        this function will raise a `ValueError` exception.
    :returns: A valid ID from the value passed to the ``_id`` parameter.
    """
    _id = _id.rstrip("-").lstrip("$-").lower()
    if re.match("^[a-z0-9\\-]+$", _id) is None:
        raise ValueError(
            "Device ID can only consist of lowercase a-z, digits 0-9, or hyphens."
        )
    return _id


class HomieProperty:
    """A class to represent a single property of a Homie device's node.

    :param name: The human friendly name of the node.
    :param datatype: The node's data type. Valid data types are defined in
        `PAYLOAD_TYPES`.
    :param property_id: A unique identifying `str` to use in the generated MQTT topic.
        If this parameter is not specified, then the ``name`` parameter will be used
        (providing it conforms to Homie specifications - see `validate_id()`).
    :param init_value: The property's initial value.

    :throws: A `ValueError` can indicate if the specified ``data_type`` or
        ``property_id`` is invalid. The exception's message will indicate which value.
    """

    def __init__(
        self,
        name: str,
        datatype: str,
        property_id: str = None,
        init_value="",
        **extra_attributes
    ):
        #: The property's human friendly ``$name`` attribute
        self.name = name
        #: The property's ``$datatype`` attribute
        assert (
            datatype.lower() in PAYLOAD_TYPES
        ), "{} datatype is not specified by Homie convention".format(datatype.lower())
        self.datatype = datatype.lower()
        #: The property's value.
        self._value = init_value
        #: The property's ID as used in the generated MQTT topic.
        self.property_id = validate_id(name if not property_id else property_id)
        for attr_name, attr_val in extra_attributes.items():
            setattr(self, attr_name, attr_val)
        self._callback = None

    def __call__(self):
        """The current value of an instantiated property can be fetched by calling the
        object directly.

        .. code-block:: python

            >>> led_property = HomieProperty("color", "color", init_value="0,255,0")
            >>> print(led_property())
            0,255,0
        """
        return self._value

    def __repr__(self):
        """Return a human friendly representation of this property."""
        return "<HomieProperty {} ({}) type {}>".format(
            self.name, self.property_id, self.datatype
        )

    def set(self, value):
        """A helper function to change the property's value. This is called by
        `HomieDevice.set_property()`.

        .. important::
            This function will not update the value on the MQTT broker.
            Instead use `HomieDevice.set_property()` to do that.

        :param value: The new value to be used as the property's value.
        :returns: A usable object as a result of validation. This class has no
            implemented validation method because it is meant to be a derivative's
            base class. Therefore, this function simply returns the specified
            ``value`` parameter.

            .. seealso:: The :doc:`helpers` have validators implemented accordingly.
        """
        self._value = value
        return value

    def is_settable(self) -> bool:
        """Can this property be manipulated from the broker?"""
        if hasattr(self, "settable"):
            return getattr(self, "settable")
        return False

    @property
    def callback(self):
        """This attribute shall hold a pointer to a callback function that
        is called when the property's value changes via broker subscription."""
        if not self.is_settable():
            return None
        if callable(self._callback):
            return self._callback
        raise NotImplementedError(
            "{} is not settable or has no callback method.".format(self)
        )

    @callback.setter
    def callback(self, method):
        if not callable(method):
            raise ValueError("The given parameter is not a method.")
        self._callback = method


class HomieNode:  # pylint: disable=too-few-public-methods
    """A class to represent a Homie device's individual node.

    :param name: The human friendly name of the node.
    :param node_type: A description of the node's type.
    :param node_id: A unique identifying `str` to use in the generated MQTT topic.
        If this parameter is not specified, then the ``name`` parameter will be used
        (providing it conforms to Homie specifications - see `validate_id()`).
    """

    def __init__(
        self, name: str, node_type: str, node_id: str = None, **extra_attributes
    ):
        #: The node's human friendly ``$name``  attribute.
        self.name = name
        #: The node's ``$type`` attribute.
        self.type = node_type
        #: The node's ID as used in the generated MQTT topic.
        self.node_id = validate_id(name if not node_id else node_id)
        #: The node's properties is a list of `HomieProperty` objects.
        self.properties = []  # type: List[HomieProperty]
        for attr_name, attr_val in extra_attributes.items():
            setattr(self, attr_name, attr_val)


class HomieDevice:
    """A class to represent an instantiated Homie device.

    :param client: An instance of an MQTT client object that the device will use to
        communicate with a MQTT broker.
    :param name: The device's human friendly name.
    :param device_id: A unique identifying string for the device. This should adhere to
        the Homie ID specifications. Meaning only lowercase letters (a-z) or numbers or
        hyphens (``-``) are allowed. This ID is prohibited from starting with a ``$``
        and cannot begin or end with a ``-``, thus these characters are stripped from
        the given input.
    """

    #: The ``$implementation`` attribute is global to all instantiated devices.
    implementation = "circuitpython on " + uname()[0]

    #: The base topic used for all Homie devices.
    base_topic = "homie"

    def __init__(self, client: MQTT, name: str, device_id: str):
        #: The MQTT client object.
        self.client = client
        #: The Homie firmware name and version in a `dict`.
        self.firmware = dict(name="circuitpython-homie", version=__version__)
        #: The list of nodes for this device.
        self.nodes = []  # type: List[HomieNode]
        self.homie = "4.0.0"
        #: The device's ``$name`` attribute.
        self.name = name
        #: The supported Homie extensions (not implemented by this library).
        self.extensions = "null.dummy:none[3.x;4.x]"
        # self.extra_attributes = {}  # type: Dict[str, Any]
        #: A flag to control interaction with Homie's ``$broadcast`` topic
        self.enable_broadcast = True

        device_id = validate_id(device_id)
        self.topic = "/".join([self.base_topic, device_id])
        try:
            if self.client.is_connected():
                self.client.disconnect()
        except MMQTTException:
            pass  # this exception meant the client is disconnected.
        self.client.will_set(self.topic + "/$state", "lost")
        self.client.connect(keep_alive=5)

    def begin(self):
        """Register this Homie device with the MQTT broker."""
        assert self.client.is_connected()
        # publish default/required attributes
        for attr in ("homie", "name", "extensions", "implementation"):
            self.client.publish(
                self.topic + "/$" + attr,
                getattr(self, attr),
                retain=True,
                qos=1,
            )
        for key, value in self.firmware.items():
            self.client.publish("/".join([self.topic, "$fw", key]), value)

        # publish this device's nodes
        self.client.publish(
            self.topic + "/$nodes",
            ",".join([node.name for node in self.nodes]),
            retain=True,
            qos=1,
        )
        for node in self.nodes:
            node_topic = "/".join([self.topic, node.node_id]) + "/"
            self.client.publish(
                node_topic + "$name",
                node.name,
                retain=True,
                qos=1,
            )
            self.client.publish(
                node_topic + "$type",
                node.type,
                retain=True,
                qos=1,
            )

            # publish this node's properties
            self.client.publish(
                node_topic + "$properties",
                ",".join([p.property_id for p in node.properties]),
                retain=True,
                qos=1,
            )
            for prop in node.properties:
                prop_topic = node_topic + prop.property_id
                for attr in dir(prop):
                    value = getattr(prop, attr)
                    if (
                        attr.startswith("_")
                        or attr in ("callback", "property_id")
                        or callable(value)
                    ):
                        continue
                    self.client.publish(
                        "/".join([prop_topic, "$" + attr]),
                        value if isinstance(value, str) else str(value).lower(),
                        retain=True,
                        qos=1,
                    )
                if prop.is_settable():
                    self.client.add_topic_callback(prop_topic + "/set", prop.callback)
                    self.client.subscribe(prop_topic + "/set", qos=1)
                self.client.publish(prop_topic, str(prop()), retain=True, qos=1)
        self.client.publish(
            self.topic + "/$state",
            "ready",
            retain=True,
            qos=1,
        )
        if self.enable_broadcast:
            self.client.subscribe(self.base_topic + "/$broadcast/#", qos=1)

    def set_state(self, state: str):
        """Set the device's state attribute on the MQTT broker.

        :param state: The new desired state of the device.
        :throws: If the specified ``state`` value is not a member of `DEVICE_STATES`,
            then a `ValueError` exception is raised.
        """
        if state not in DEVICE_STATES:
            raise ValueError("Given state {} is not Homie compliant".format(state))
        if self.client.is_connected():
            self.client.publish(self.topic + "/$state", state, retain=True, qos=1)

    def set_property(self, prop: HomieProperty, value, multi_node: bool = False):
        """Change a specified property's value and publish it to the MQTT broker.

        :param prop: the instance object representing the device node's property.
        :param multi_node: Set this to `True` if the property is associated with
            multiple device nodes. By default, only the first node found in
            association is updated on the MQTT broker.
        :throws: If the property is not associated with one of the device's `nodes`,
            then a `ValueError` exception is raised.
        """
        actual_val = prop.set(value)
        pub_val = prop() if isinstance(prop(), str) else str(prop())
        for node in self.nodes:
            if prop in node.properties:
                topic = "/".join([self.topic, node.node_id, prop.property_id])
                self.client.publish(topic, pub_val)
                if not multi_node:
                    break
        else:
            raise ValueError(
                "Could not find the node associated with the given property: {}".format(
                    prop
                )
            )
        return actual_val
