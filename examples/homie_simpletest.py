"""A simple example of OpenHab controlling the on-board LED.

This was tested on:

- UnexpectedMaker FeatherS2 board (with a dotstar)
- Adafruit QtPy ESP32-S2 (with a neopixel)
"""
# pylint: disable=import-error,no-member,unused-argument,invalid-name
import time
import board
import socketpool  # type: ignore
import wifi  # type: ignore
from adafruit_minimqtt.adafruit_minimqtt import MQTT, MMQTTException
from circuitpython_homie import HomieDevice, HomieNode
from circuitpython_homie.recipes import PropertyRGB

if not hasattr(board, "NEOPIXEL"):
    # assume board has a builtin dotstar
    import adafruit_dotstar

    pixel = adafruit_dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1)
else:
    import neopixel

    pixel = neopixel.NeoPixel(board.NEOPIXEL, 1)

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

# create the objects that describe our device
device = HomieDevice(mqtt_client, "my device name", "lib-simple-test-id")
led_node = HomieNode("light", "RGB DotStar")
led_property = PropertyRGB("color", settable=True)

# append the objects to the device's attributes
led_node.properties.append(led_property)
device.nodes.append(led_node)

pixel.fill(led_property.value)  # color the LED with the property's value

# add a callback to remotely control the LED
def change_color(client: MQTT, topic: str, message: str):
    """Change the color of the LED based on the message from the broker."""
    print("--> broker said color is now", message)
    # echo confirmation back to broker and convert to an 3-tuple of integers
    color = device.set_property(led_property, message)
    pixel.fill(color)
    print("<-- color is now", repr(color))


led_property.callback = change_color


def on_disconnected(client: MQTT, user_data, rc):
    """Callback invoked when connection to broker is terminated."""
    print("Reconnecting to the broker.")
    client.reconnect()
    device.set_state("ready")


mqtt_client.on_disconnect = on_disconnected
mqtt_client.on_connect = lambda *args: print("Connected to the MQTT broker!")

# connect to the broker and publish/subscribe the device's topics
device.begin(keep_alive=3000)
# keep_alive must be set to avoid the device's `$state` being considered "lost"

# a forever loop
try:
    refresh_last = time.time()
    while True:
        try:
            now = time.time()
            if now - refresh_last > 0.5:  # refresh every 0.5 seconds
                refresh_last = now
                mqtt_client.loop()
        except MMQTTException:
            print("!!! Connection with broker is lost.")
except KeyboardInterrupt:
    device.set_state("disconnected")
    mqtt_client.on_disconnect = lambda *args: print("Disconnected from broker")
    mqtt_client.deinit()
