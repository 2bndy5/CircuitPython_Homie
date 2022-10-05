"""A simple example of broadcasting a DHT11 sensor's data.

This was tested on a Adafruit QtPy ESP32-S2.
"""
# pylint: disable=import-error,no-member,unused-argument,invalid-name
import time
import board
import socketpool  # type: ignore
import wifi  # type: ignore
from adafruit_minimqtt.adafruit_minimqtt import MQTT, MMQTTException
import adafruit_dht
from circuitpython_homie import HomieDevice, HomieNode
from circuitpython_homie.recipes import PropertyFloat, PropertyPercent

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
dht_in = board.A0  # change this accordingly
dht_sensor = adafruit_dht.DHT11(dht_in)
dht_sensor.measure()  # update current data for Homie init

# create the objects that describe our device
device = HomieDevice(mqtt_client, "my device name", "lib-dht-sensor-test-id")
dht_node = HomieNode("DHT11", "temperature/humidity sensor")
dht_temperature_property = PropertyFloat(
    "temperature", init_value=dht_sensor.temperature * (9 / 5) + 32, unit="°F"
)
dht_humidity_property = PropertyPercent(
    "humidity", datatype="integer", init_value=dht_sensor.humidity
)

# append the objects to the device's attributes
dht_node.properties.extend([dht_temperature_property, dht_humidity_property])
device.nodes.append(dht_node)


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
            if now - refresh_last > 2:  # refresh every 2 seconds
                refresh_last = now
                mqtt_client.loop()
                dht_sensor.measure()  # update current data
                temp = device.set_property(
                    dht_temperature_property, dht_sensor.temperature * (9 / 5) + 32
                )
                print("Temp:", temp, dht_temperature_property.unit[-1], end=" ")
                humid = device.set_property(dht_humidity_property, dht_sensor.humidity)
                print("Humidity:", humid, dht_humidity_property.unit, end="\r")
        except MMQTTException:
            print("\n!!! Connection with broker is lost.")
except KeyboardInterrupt:
    device.set_state("disconnected")
    print()  # move cursor to next line
    mqtt_client.on_disconnect = lambda *args: print("Disconnected from broker")
    mqtt_client.deinit()
    dht_sensor.exit()
