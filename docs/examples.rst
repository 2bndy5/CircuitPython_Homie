Examples
========

All of these examples require a separate user-defined module named secrets.py
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
    )

Simple test
------------

Ensure your device works with this simple test.

.. literalinclude:: ../examples/homie_simpletest.py
    :caption: examples/homie_simpletest.py
    :linenos:
