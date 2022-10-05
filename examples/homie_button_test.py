"""A simple example of OpenHab manipulating a boolean state changed by the
on-board button. As a form of visual feedback, the on-board LED is used to
reflect the boolean state.

This was tested on:

- UnexpectedMaker FeatherS2 board (with a dotstar)
- Adafruit QtPy ESP32-S2 (with a neopixel)
"""
# pylint: disable=import-error,no-member,unused-argument,invalid-name
import time
import board
import digitalio
import socketpool  # type: ignore
import wifi  # type: ignore
from adafruit_minimqtt.adafruit_minimqtt import MQTT, MMQTTException
from circuitpython_homie import HomieDevice, HomieNode
from circuitpython_homie.recipes import PropertyBool

if not hasattr(board, "NEOPIXEL"):
    # assume board has a builtin dotstar
    import adafruit_dotstar

    pixel = adafruit_dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1)
else:
    import neopixel

    pixel = neopixel.NeoPixel(board.NEOPIXEL, 1)
pixel.brightness = 0.5  # go easy on the eyes
pixel.fill((255, 0, 0))  # this example's initial value of the switch state is False

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

# instantiate the button and it's state
# declare the state as a list because using `global` is a bad habit
button_pin = board.BUTTON  # change this accordingly
button = digitalio.DigitalInOut(button_pin)
button.switch_to_input(digitalio.Pull.UP)
button_value = button.value  # for edge detection

# create the objects that describe our device
device = HomieDevice(mqtt_client, "my device name", "lib-button-id")
switch_node = HomieNode("light", "Typical Lamp")
switch_property = PropertyBool("switch", settable=True)

# append the objects to the device's attributes
switch_node.properties.append(switch_property)
device.nodes.append(switch_node)

# add a callback to remotely control the switch_property
def change_state(client: MQTT, topic: str, message: str):
    """Change the switch's state according to message from the broker."""
    print("--> broker said switch_state is now", message)
    # echo confirmation back to broker
    switch_state = device.set_property(switch_property, message)
    pixel.fill((0, 255, 0) if switch_state else (255, 0, 0))
    print("<-- switch state is now", switch_state)


switch_property.callback = change_state


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
            # toggle the switch's state on button press
            if button_value != button.value and not button.value:
                button_value = button.value
                state = device.set_property(switch_property, not switch_property.value)
                print("button was pressed", "<(!)>" if state else " (-) ")
                pixel.fill((0, 255, 0) if state else (255, 0, 0))
            elif button.value and button_value != button.value:
                button_value = button.value
            now = time.time()
            if now - refresh_last >= 1:  # refresh every 1 seconds
                refresh_last = now
                assert mqtt_client.is_connected()
                mqtt_client.loop()
        except MMQTTException:
            print("!!! Connection with broker is lost.")
except KeyboardInterrupt:
    device.set_state("disconnected")
    mqtt_client.on_disconnect = lambda *args: print("Disconnected from broker")
    mqtt_client.deinit()
