"""pytest config file"""
import json
from pathlib import Path
from typing import Dict, Any, Union, List, cast, Tuple, Callable
import pytest
from circuitpython_homie import HomieDevice, HomieNode
from circuitpython_homie.recipes import PropertyBool, PropertyRGB, PropertyInt

PAYLOAD_TYPE = Union[str, bytes, bytearray]


class ShimMQTT:
    """A shim implementation of an MQTT client designed to mimic
    `adafruit_minimqtt.adafruit_minimqtt.MQTT` class."""

    def __init__(self, host: str, port: int = 1883) -> None:
        self.host, self.port = (host, port)
        self._connected = True  # just for better coverage
        self._log: Dict[str, Any] = dict(publish=[], subscribe=[])
        self.keep_alive = 0

    def is_connected(self) -> bool:
        """Is the client connected to the broker?"""
        # raise MMQTTException("client is not connected")
        return self._connected

    def connect(self, host: str = None, port: int = None, keep_alive: int = None):
        """Fake a connection to a non-existent broker."""
        self._connected = True
        if host:
            self.host = host
        if port is not None:
            self.port = port
        if keep_alive is not None:
            self.keep_alive = keep_alive

    def disconnect(self):
        """Fake a disconnection from a non-existent broker."""
        self._connected = False

    def will_set(self, topic: PAYLOAD_TYPE, message: PAYLOAD_TYPE, qos: int = 0):
        """Set a will and Testament before calling `connect()`.

        For testing purposes, this will raise a runtime error if already connected.
        """
        self._log["will-n-testament"] = dict(topic=topic, message=message, qos=qos)
        if self._connected:
            raise RuntimeError("Cannot set a Will/Testament while connected")

    def publish(
        self,
        topic: PAYLOAD_TYPE,
        message: PAYLOAD_TYPE,
        retain: bool = False,
        qos: int = 0,
    ):
        """Pseudo-publish a topic's message to non-existent broker."""
        if not isinstance(topic, (str, bytes, bytearray)):
            raise ValueError("topic is not a bytes, bytearray, or str object")
        if not isinstance(message, (str, bytes, bytearray)):
            raise ValueError("message is not a bytes, bytearray, or str object")
        log = dict(topic=topic, message=message, qos=qos, retain=retain)
        cast(List[dict], self._log["publish"]).append(log)

    def subscribe(self, topic: PAYLOAD_TYPE, qos: int = 0):
        """Pseudo-subscribe a topic's message to non-existent broker."""
        if not isinstance(topic, (str, bytes, bytearray)):
            raise ValueError("topic is not a bytes, bytearray, or str object")
        log = dict(topic=topic, qos=qos)
        cast(List[dict], self._log["subscribe"]).append(log)

    def add_topic_callback(
        self, topic: PAYLOAD_TYPE, _cb: Callable[["ShimMQTT", str, str], None]
    ):
        """Pseudo-register a callback with a given topic."""
        self._log["callback-registry"] = dict(topic=topic, method=_cb.__name__)

    def export_logs(self):
        """Export aggregated logs to JSON file."""
        (Path.cwd() / "fake-mqtt-log.json").write_text(
            json.dumps(self._log, indent=2), encoding="utf-8"
        )


@pytest.fixture(scope="module")
def created_shim_dev() -> HomieDevice:
    """A fixture to create a `HomieDevice` object filled with nodes and properties."""
    client = ShimMQTT("non_existent_server", 5555)
    dev = HomieDevice(client, "shim test device", "test-device")

    mood_node = HomieNode("mood", "mood descriptive color")
    heater_node = HomieNode("heater", "A space heater")
    thermostat_node = HomieNode("thermostat", "temperature sensor")

    thermostat_prop = PropertyInt("temperature")
    heater_prop = PropertyBool("switch", settable=True)
    mood_prop = PropertyRGB("color", retained=False)

    def flip_switch(*args: Tuple[ShimMQTT, str, str]):
        """called when broker flips the switch property's value."""
        dev.set_property(heater_prop, args[2])

    heater_prop.callback = flip_switch

    dev.nodes.extend([mood_node, heater_node, thermostat_node])
    mood_node.properties.append(mood_prop)
    heater_node.properties.append(heater_prop)
    thermostat_node.properties.append(thermostat_prop)

    return dev
