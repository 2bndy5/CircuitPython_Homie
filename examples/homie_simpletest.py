"""A simple example of OpenHab controlling the on-board dotstar.

This was tested on a UnexpectedMaker FeatherS2 board.
"""
# pylint: disable=import-error,no-member,unused-argument
import time
import board
import socketpool  # type: ignore
import wifi  # type: ignore
import adafruit_dotstar
from adafruit_minimqtt.adafruit_minimqtt import MQTT
from circuitpython_homie import HomieDevice
from circuitpython_homie.nodes import HomieNode
from circuitpython_homie.properties import HomieProperty

# Get wifi details and more from a secrets.py file
try:
    from secrets import wifi_settings, mqtt_settings
except ImportError as exc:
    raise RuntimeError(
        "WiFi and MQTT secrets are kept in secrets.py, please add them there!"
    ) from exc

print("Connecting to", wifi_settings["ssid"])
wifi.radio.connect(**wifi_settings)
print("Connected successfully!")
print("My IP address is", wifi.radio.ipv4_address)

print("Using MQTT broker: {}:{}".format(mqtt_settings["broker"], mqtt_settings["port"]))
pool = socketpool.SocketPool(wifi.radio)
mqtt_client = MQTT(**mqtt_settings, socket_pool=pool)
device = HomieDevice(mqtt_client, "my device name", "unique-device-id")
led_node = HomieNode("light", "RGB DotStar")
led_property = HomieProperty(
    "color", "color", settable=True, format="rgb", init_value="0,0,0"
)
led_node.properties.append(led_property)
device.nodes.append(led_node)

pixel = adafruit_dotstar.DotStar(
    board.APA102_SCK,
    board.APA102_MOSI,
    1,
)

# add a callback to remotely control the LED
def change_color(client, topic: str, message: str):
    """A callback function used to receive color changes from the MQTT broker."""
    print("broker said color is now", message)
    color = tuple(int(x) for x in message.split(","))
    print("color is now", repr(color))
    pixel.fill(color)
    device.set_property(led_property, message)


led_property.callback = change_color

# connect to the broker and publish/subscribe the device's topics
device.begin()
print("Connected to the MQTT broker!")

try:
    refresh_last = time.time()
    while True:
        now = time.time()
        if now - refresh_last > 2:  # refresh every 2 seconds
            # print("refreshing MQTT broker events")
            refresh_last = now
            assert mqtt_client.is_connected()
            mqtt_client.loop()
            refresh_last = now
except KeyboardInterrupt:
    device.set_state("disconnected")
