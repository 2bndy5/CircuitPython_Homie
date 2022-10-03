Examples
========

Prerequisites
-------------

All of these examples require a separate user-defined module named ``secrets.py``.
In this secrets module should be 2 `dict`\ s:

1. ``wifi_settings`` consisting of parameter names and values for the WiFi configuration.
2. ``mqtt_settings`` consisting of parameter names and values for the MQTT broker configuration.

.. code-block:: python
    :caption: secrets.py

    """
    This file is where you keep secret settings, passwords, and tokens!
    If you put them in the code you risk committing that info or sharing it
    """

    wifi_settings = dict(
        ssid = "WiFi_Network_Name",
        password = "WiFi_Password",
    )

    mqtt_settings = dict(
        broker="openhabian",  # the broker's hostname or IP address
        port=1883,  # the broker's port
        username="user_name",
        password="user_password",
    )

The MQTT username and password may not be required if you skipped :ref:`mqtt_user_password`.

Dependencies
************

Some examples use other third-party libraries (which are available in Adafruit's CircuitPython
Library bundle). These libraries are listed in the examples/requirements.txt file for easy install.

.. literalinclude:: ../examples/requirements.txt
    :caption: examples/requirements.txt

Simple test
------------

Ensure your device works with this simple test.

This example uses the `PropertyRGB` class to represent the on-board LED (Neopixel or Dotstar).
The color is controlled using OpenHAB_.

.. literalinclude:: ../examples/homie_simpletest.py
    :caption: examples/homie_simpletest.py
    :linenos:
    :start-after: pylint: disable=import-error
    :lineno-match:

Light Sensor test
-----------------

Demonstrates using the `PropertyPercent` class to represent a light sensor's data.

.. literalinclude:: ../examples/homie_light_sensor_test.py
    :caption: examples/homie_light_sensor_test.py
    :linenos:
    :start-after: pylint: disable=import-error
    :lineno-match:

DHT Sensor test
-----------------

Demonstrates using the `PropertyPercent` and `PropertyFloat` classes to represent a DHT11 sensor's
humidity and temperature data (respectively).

.. literalinclude:: ../examples/homie_dht_sensor_test.py
    :caption: examples/homie_dht_sensor_test.py
    :linenos:
    :start-after: pylint: disable=import-error
    :lineno-match:

Clock test
------------

A simple clock app that broadcasts the current date and time using the `PropertyDateTime` class.

The real time clock is synchronized using the `adafruit_ntp` library.

.. literalinclude:: ../examples/homie_clock_test.py
    :caption: examples/homie_clock_test.py
    :linenos:
    :start-after: pylint: disable=import-error
    :lineno-match:

button test
------------

A simple app that broadcasts the state of a switch using the `PropertyBool` class.

The on-board LED is used as visual feedback (to emulate a lamp).

.. literalinclude:: ../examples/homie_button_test.py
    :caption: examples/homie_button_test.py
    :linenos:
    :start-after: pylint: disable=import-error
    :lineno-match:
