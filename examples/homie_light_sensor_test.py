"""A simple example of broadcasting a light sensor's data as a percentage.

This was tested on a UnexpectedMaker FeatherS2 board.
"""
# pylint: disable=import-error,no-member,unused-argument,invalid-name
import time
import analogio
import board
import socketpool  # type: ignore
import wifi  # type: ignore
from adafruit_minimqtt.adafruit_minimqtt import MQTT, MMQTTException
from circuitpython_homie import HomieDevice, HomieNode
from circuitpython_homie.recipes import PropertyPercent

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

# create a light_sensor object for analog readings
light_sensor_pin = board.IO4  # change this accordingly
light_sensor = analogio.AnalogIn(light_sensor_pin)

# create the objects that describe our device
device = HomieDevice(mqtt_client, "my device name", "lib-light-sensor-test-id")
ambient_light_node = HomieNode("ambient-light", "Light Sensor")
ambient_light_property = PropertyPercent("brightness")

# append the objects to the device's attributes
ambient_light_node.properties.append(ambient_light_property)
device.nodes.append(ambient_light_node)


def on_disconnected(client: MQTT, user_data, rc):
    """Callback invoked when connection to broker is terminated."""
    print("Reconnecting to the broker.")
    client.reconnect()
    device.set_state("ready")


mqtt_client.on_disconnect = on_disconnected
mqtt_client.on_connect = lambda *args: print("Connected to the MQTT broker!")

# connect to the broker and publish/subscribe the device's topics
device.begin()

# a forever loop
try:
    refresh_last = time.time()
    while True:
        try:
            now = time.time()
            if now - refresh_last > 0.5:  # refresh every 0.5 seconds
                refresh_last = now
                assert mqtt_client.is_connected()
                value = device.set_property(
                    ambient_light_property, light_sensor.value / 65535 * 100
                )
                print("light sensor value:", value, end="\r")
        except MMQTTException:
            print("\n!!! Connection with broker is lost.")
except KeyboardInterrupt:
    device.set_state("disconnected")
    print()  # move cursor to next line
    mqtt_client.on_disconnect = lambda *args: print("Disconnected from broker")
    mqtt_client.disconnect()
