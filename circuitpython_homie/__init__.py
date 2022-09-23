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
    from typing import TYPE_CHECKING, List, Union, Dict, Any

    if TYPE_CHECKING:  # avoids cyclical imports
        # import paho.mqtt.client as mqtt
        from .nodes import HomieNode
except ImportError:
    pass  # don't type check on CircuitPython firmware

from adafruit_minimqtt.adafruit_minimqtt import MQTT, MMQTTException
from .properties import HomieProperty
from .helpers import validate_id, DEVICE_STATES

__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/2bndy5/CircuitPython_Homie.git"


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
        #: The Homie firmware name.
        self.fw_name = "circuitpython-homie"
        #: The list of nodes for this device.
        self.nodes = []  # type: List[HomieNode]
        self.homie = "4.0.0"
        #: The device's ``$name`` attribute.
        self.name = name
        #: The supported Homie extensions (not implemented by this library).
        self.extensions = ""
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
        self.client.connect(keep_alive=2)

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
                        or callable(value)
                        or attr in ("callback", "property_id")
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

        :param state: The new desired state of the device. This value should be a
            member of `DEVICE_STATES`
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
        pub_val = value if isinstance(value, str) else str(value)
        for node in self.nodes:
            if prop in node.properties:
                topic = "/".join([self.topic, node.node_id, prop.property_id])
                print("publishing to topic", topic)
                self.client.publish(topic, pub_val)
                prop.set(value)
                if not multi_node:
                    break
        else:
            raise ValueError(
                "Could not find the node associated with the given property: {}".format(
                    prop
                )
            )
