"""A simple example of broadcasting a date and time.

This was tested on:

- UnexpectedMaker FeatherS2 board (with a dotstar)
- Adafruit QtPy ESP32-S2 (with a neopixel)
- A Windows PC
"""
# pylint: disable=import-error,no-member,unused-argument,invalid-name,used-before-assignment
import time

try:
    import socket

    CIR_PY = False
except ImportError:
    CIR_PY = True

    import socketpool  # type: ignore
    import wifi  # type: ignore
    import rtc  # type: ignore

from adafruit_minimqtt.adafruit_minimqtt import MQTT, MMQTTException
from adafruit_ntp import NTP
from circuitpython_homie import HomieDevice, HomieNode
from circuitpython_homie.recipes import PropertyDateTime

# Get wifi details and more from a secrets.py file
try:
    from secrets import wifi_settings, mqtt_settings
except ImportError as exc:
    raise RuntimeError(
        "WiFi and MQTT secrets are kept in secrets.py, please add them there!"
    ) from exc

if CIR_PY:  # only on CircuitPython
    print("Connecting to", wifi_settings["ssid"])
    wifi.radio.connect(**wifi_settings)
    print("Connected successfully!")
    print("My IP address is", wifi.radio.ipv4_address)

    pool = socketpool.SocketPool(wifi.radio)

    # adjust this according to your time zone
    # https://en.wikipedia.org/wiki/List_of_time_zone_abbreviations
    TIME_ZONE = -7  # for Mountain Standard Time (North America)
    ntp = NTP(pool, tz_offset=TIME_ZONE)

    # sync the system clock (accessible via `time.localtime()`)
    rtc.RTC().datetime = ntp.datetime
else:  # on CPython
    print("My IP address is", socket.gethostbyname(socket.gethostname()))

print("Using MQTT broker: {}:{}".format(mqtt_settings["broker"], mqtt_settings["port"]))
if CIR_PY:  # only on CircuitPython
    mqtt_client = MQTT(**mqtt_settings, socket_pool=pool)
else:  # on CPython
    mqtt_client = MQTT(**mqtt_settings, socket_pool=socket)

# create the objects that describe our device
device = HomieDevice(mqtt_client, "my device name", "lib-clock-test-id")
clock_node = HomieNode("clock", "clock")
clock_property = PropertyDateTime(
    "current-time",
    init_value=PropertyDateTime.convert(time.localtime()),
)

# append the objects to the device's attributes
clock_node.properties.append(clock_property)
device.nodes.append(clock_node)


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
    time_fmt = clock_property.convert(time.localtime())
    while True:
        try:
            now = time.time()
            print(time_fmt, end="\r")
            if now - refresh_last >= 1:  # refresh every 1 second
                refresh_last = now
                assert mqtt_client.is_connected()
                time_fmt = device.set_property(clock_property, time.localtime())
        except MMQTTException:
            print("\n!!! Connection with broker is lost.")
except KeyboardInterrupt:
    device.set_state("disconnected")
    print()  # move cursor to next line
    mqtt_client.on_disconnect = lambda *args: print("Disconnected from broker")
    mqtt_client.deinit()
