# SPDX-FileCopyrightText: Copyright (c) 2022 Brendan Doherty
#
# SPDX-License-Identifier: MIT
"""
The :mod:`circuitpython_homie` module holds the Homie implementations for a
:class:`device <HomieDevice>`, :class:`node <HomieNode>`, and
:class:`property <HomieProperty>`. See the :mod:`circuitpython_homie.recipes` module
for specialized properties that implement certain datatypes defined by the
`Homie Specifications <https://homieiot.github.io/specification#payload>`_.
"""
try:
    from os import uname  # type: ignore
except ImportError:
    from platform import uname  # type: ignore

try:
    from typing import List, Dict, Any
except ImportError:
    pass  # don't type check on CircuitPython firmware

import re
from adafruit_minimqtt.adafruit_minimqtt import MQTT, MMQTTException  # type: ignore


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

.. hlist::

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
    :param datatype: The node's :homie-attr:`datatype`. Valid data types are defined in
        `PAYLOAD_TYPES`. Default is :python:`"string"`.
    :param property_id: A unique identifying `str` to use in the generated MQTT topic.
        If this parameter is not specified, then the ``name`` parameter will be used
        (providing it conforms to Homie specifications - see `validate_id()`).
    :param init_value: The property's initial value.

    :throws: A `ValueError` can indicate if the specified ``datatype`` or
        ``property_id`` is invalid. The exception's message will indicate which value.

    .. warning:: All attributes for this class should be considered read-only after
        calling `HomieDevice.begin()`. This is because the attributes published to the
        MQTT broker are not dynamically updated without calling `HomieDevice.begin()`
        after changing the attributes' value.
    """

    def __init__(
        self,
        name: str,
        datatype: str = "string",
        property_id: str = None,
        init_value="",
        **extra_attributes
    ):
        #: The property's human friendly :homie-attr:`name` attribute
        self.name = name
        datatype = datatype.lower()
        if datatype not in PAYLOAD_TYPES:
            raise ValueError("{} datatype is not in {}".format(datatype, PAYLOAD_TYPES))
        #: The property's :homie-attr:`datatype` attribute.
        self.datatype = datatype
        #: The property's value.
        self._value = init_value
        #: The property's ID as used in the generated MQTT topic.
        self.property_id = validate_id(name if not property_id else property_id)
        if "settable" in extra_attributes:
            assert isinstance(extra_attributes.get("settable"), bool)
        if "retained" in extra_attributes:
            assert isinstance(extra_attributes.get("retained"), bool)
        for attr_name, attr_val in extra_attributes.items():
            setattr(self, attr_name, attr_val)
        self._callback = None

    @property
    def value(self):
        """The current value of the property.

        .. admonition:: Read Only
            :class: missing

            This function will not update the value on the MQTT broker.
            Instead use `HomieDevice.set_property()` to do that.

        :returns: A usable object as a result of validation. This class has no
            implemented validation method because it is meant to be a derivative's
            base class. Therefore, this function simply returns the specified
            value.

            .. seealso:: The :doc:`recipes` have validators implemented accordingly.
        """
        return self._value

    def __repr__(self):
        """Return a human friendly representation of this property."""
        return "<HomieProperty {} type {}>".format(self.property_id, self.datatype)

    def __str__(self) -> str:
        return self.property_id

    def _set(self, value):
        """A helper function to change the property's value. This is called by
        `HomieDevice.set_property()`."""
        self._value = value
        return value

    def is_settable(self) -> bool:
        """Can this property be manipulated from the broker? This is controlled by the
        declaring a :homie-attr:`settable` `bool` attribute. By default, all properties
        are not settable.

        .. code-block:: python

            >>> prop1 = HomieProperty("demo-1")
            >>> prop1.is_settable()
            False
            >>> prop2 = HomieProperty("demo-2", settable=True)
            >>> prop2.is_settable()
            True
        """
        if hasattr(self, "settable"):
            return getattr(self, "settable")
        return False

    def is_retained(self) -> bool:
        """By default, all properties are published as retained topics. This can be
        controlled by declaring a :homie-attr:`retained` `bool` attribute.

        .. code-block:: python

            >>> prop1 = HomieProperty("demo-1")
            >>> prop1.is_retained()
            True
            >>> prop2 = HomieProperty("demo-2", retained=False)
            >>> prop2.is_retained()
            False
        """
        if hasattr(self, "retained"):
            return getattr(self, "retained")
        return True

    @property
    def callback(self):
        """This attribute shall hold a pointer to a callback function that
        is called when the property's value changes via broker subscription.

        Conventionally, this will require echoing the data back to the broker as
        confirmation.

        .. seealso::
            Use `HomieDevice.set_property()` to echo back a confirmation to the MQTT
            broker.
        .. code-block:: python

            prop1 = HomieProperty("signage", settable=True)

            def new_signage(client: MQTT, topic, :str, message: str):
                # let `my_device` be the instantiated HomieDevice object
                my_device.set_property(prop1, message)  # confirm with broker
                # Optionally do something with the new value
                print("received:", prop1.value)

            prop1.callback = new_signage
        .. details:: Using a lambda
            :class: info

            CircuitPython also supports `lambda` objects.

            .. code-block:: python

                prop2 = HomieProperty("signage", settable=True)
                prop2.callback = lambda *args: my_device.set_property(prop2, args[2])

            This assumes that the property's `value` will be used elsewhere.
        """
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
    :param node_type: A description of the node's :homie-attr:`type`.
    :param node_id: A unique identifying `str` to use in the generated MQTT topic.
        If this parameter is not specified, then the ``name`` parameter will be used
        (providing it conforms to Homie specifications - see `validate_id()`).

    .. warning:: All attributes for this class should be considered read-only after
        calling `HomieDevice.begin()`. This is because the attributes published to the
        MQTT broker are not dynamically updated without calling `HomieDevice.begin()`
        after changing the attributes' value.
    """

    def __init__(self, name: str, node_type: str, node_id: str = None):
        #: The node's human friendly :homie-attr:`name` attribute.
        self.name = name
        #: The node's :homie-attr:`type` attribute.
        self.type = node_type
        #: The node's ID as used in the generated MQTT topic.
        self.node_id = validate_id(name if not node_id else node_id)
        #: The node's :homie-attr:`properties` is a list of `HomieProperty` objects.
        self.properties = []  # type: List[HomieProperty]

    def __repr__(self):
        """Return a human friendly representation of this property."""
        return "<HomieNode {}>".format(self.node_id)

    def __str__(self) -> str:
        return self.node_id


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

    implementation = "CircuitPython on " + uname()[0]
    """The :homie-attr:`implementation` attribute used for all `HomieDevice` instances
    (class attribute). The platform specified by default is taken from
    :attr:`~os._Uname.sysname`.
    """

    #: The base topic used for all `HomieDevice` instances (class attribute).
    base_topic = "homie"

    def __init__(self, client: MQTT, name: str, device_id: str):
        #: The MQTT client object.
        self.client = client
        #: The Homie firmware name and version in a `dict`.
        self.fw = dict(  # pylint: disable=invalid-name
            name="circuitpython-homie", version=__version__
        )
        #: The list of :homie-attr:`nodes` for this device.
        self.nodes = []  # type: List[HomieNode]
        self.homie = "4.0.0"
        #: The device's :homie-attr:`name` attribute.
        self.name = name
        #: The supported Homie extensions (not implemented by this library).
        self.extensions = ["null.dummy:none"]
        # self.extra_attributes = {}  # type: Dict[str, Any]
        #: A flag to control interaction with Homie's :homie-attr:`broadcast` topic.
        self.enable_broadcast = True

        device_id = validate_id(device_id)
        self.topic = "/".join([self.base_topic, device_id])

    def _publish_topic(self, topic: str, value, retain: bool = True):
        """A helper to publish topics arbitrarily."""
        if isinstance(value, dict):
            for key, val in value.items():
                self._publish_topic("/".join([topic, key]), val, retain=retain)
            return
        pub_val = value  # use a copy for normalization
        if isinstance(value, (list, tuple)):
            pub_val = ",".join([str(val) for val in value])
        elif isinstance(value, bool):
            pub_val = str(value).lower()
        if not isinstance(pub_val, str):
            pub_val = str(pub_val)
        self.client.publish(topic, pub_val, retain=retain, qos=1)

    def begin(self, **mqtt_settings):
        """Register this Homie device with the MQTT broker.

        :param mqtt_settings: All keyword arguments are used as parameters that get
            passed to :meth:`~adafruit_minimqtt.adafruit_minimqtt.MQTT.connect()`.
        """
        # set the will and testament (requires being disconnected first)
        try:
            if self.client.is_connected():
                self.client.disconnect()
        except MMQTTException:  # pragma: no cover
            pass  # this exception meant the client was disconnected.
        self.client.will_set(self.topic + "/$state", "lost")
        self.client.connect(**mqtt_settings)

        # publish default/required attributes
        for attr in ("homie", "name", "extensions", "implementation", "nodes", "fw"):
            self._publish_topic(self.topic + "/$" + attr, getattr(self, attr))

        # publish this device's nodes
        for node in self.nodes:
            node_topic = "/".join([self.topic, str(node)]) + "/"
            for attr in ("name", "type", "properties"):
                self._publish_topic(node_topic + "$" + attr, getattr(node, attr))

            # publish this node's properties
            for prop in node.properties:
                prop_topic = node_topic + prop.property_id
                retained = prop.is_retained()
                for attr in dir(prop):
                    value = getattr(prop, attr)
                    if (
                        attr.startswith("_")
                        or attr in ("callback", "property_id", "value")
                        or callable(value)
                    ):
                        continue
                    self._publish_topic(
                        "/".join([prop_topic, "$" + attr]), value, retain=retained
                    )
                if prop.is_settable():
                    self.client.add_topic_callback(prop_topic + "/set", prop.callback)
                    self.client.subscribe(prop_topic + "/set", qos=1)
                self._publish_topic(prop_topic, prop.value, retain=retained)
        if self.enable_broadcast:
            self.client.subscribe(self.base_topic + "/$broadcast/#", qos=1)
        self._publish_topic(self.topic + "/$state", "ready")

    def set_state(self, state: str):
        """Set the device's :homie-attr:`state` attribute on the MQTT broker.

        :param state: The new desired state of the device.
        :throws: If the specified ``state`` value is not a member of `DEVICE_STATES`,
            then a `ValueError` exception is raised.
        """
        if state not in DEVICE_STATES:
            raise ValueError("The state {} is not Homie compliant".format(state))
        if self.client.is_connected():
            self.client.publish(self.topic + "/$state", state, retain=True, qos=1)

    def set_property(self, prop: HomieProperty, value, multi_node: bool = False):
        """Change a specified property's value and publish it to the MQTT broker.

        :param prop: the instance object representing the device node's property.
        :param value: The new value for the property. The data type passed here will
            depend on the type of `HomieProperty` (specified by the ``prop`` parameter)
            for which it is being applied.

            .. seealso:: The :doc:`recipes` have derivatives of the `HomieProperty`
                class with validators implemented accordingly.
        :param multi_node: Set this to `True` if the property is associated with
            multiple device `nodes`. By default, only the first node found in
            association is updated on the MQTT broker.
        :throws: If the property is not associated with one of the device's `nodes`,
            then a `ValueError` exception is raised.
        """
        pub_val = prop._set(value)  # pylint: disable=protected-access
        found = False
        for node in self.nodes:
            if prop in node.properties:
                topic = "/".join([self.topic, node.node_id, str(prop)])
                self._publish_topic(topic, pub_val, prop.is_retained())
                found = True
                if not multi_node:
                    break
        if not found:
            raise ValueError("Could not find a node associated with {}".format(prop))
        return pub_val
