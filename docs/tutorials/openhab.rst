Using Homie with OpenHAB_
=========================


OpenHAB_ is a Java based software that can be used on a computer connected to your Local Area
Network (LAN) to monitor (or control) various "smart devices" in your home (or building).
Typically, it is meant to be installed to a headless machine like a Raspberry Pi, but any
computer you have sitting around should work. The machine needs to always be running and
connected to your LAN.

Prerequisite
------------

1. Install OpenHAB_ via `their excellent download instructions <https://www.openhab.org/download/>`_.
2. :doc:`mosquitto` and configure it to use your LAN.

I highly recommend following the
`OpenHAB Getting Started instructions <https://www.openhab.org/docs/tutorial/first_steps.html>`_
to get a feel for using the interface.

.. _MQTT binding: https://www.openhab.org/addons/bindings/mqtt/
.. _MQTT Homie binding: https://www.openhab.org/addons/bindings/mqtt.homie/

Adding the `MQTT binding`_
---------------------------

Building off `OpenHAB's "Add a Simple Thing" instructions
<https://www.openhab.org/docs/tutorial/things_simple.html>`_, look for a `MQTT binding`_ in the
"bindings add-ons" list.

.. md-admonition::
    :class: info

    Installing the `MQTT binding`_ in OpenHAB will also install Homie support automatically. More info
    about Homie support can be found at the `MQTT Homie binding`_ page.

    .. md-admonition::
        :class: missing

        The OpenHAB `MQTT Homie binding`_ will say that it supports Homie v3.x specifications. This library
        implements Homie v4 specifications. Homie v4 is mostly backward compatible with Homie v3 with
        the following exceptions:

        - `Node Arrays <https://homieiot.github.io/specification/spec-core-v3_0_1/#arrays>`_
          are not supported in Homie v4
        - `Device Statistics <https://homieiot.github.io/specification/spec-core-v3_0_1/#device-statistics>`_
          are not supported in Homie v4

        These missing features are memory and process intensive for microcontrollers. At this time,
        there are no plans to add Homie v3 support for this library.

Be sure to enter the hostname or IP address to the settings for the MQTT binding. Typically, the
same machine can be used for serving OpenHAB and the MQTT broker. If you're using the openhabian
OS installed on a Raspberry Pi, then the hostname will be ``openhabian``.

.. details:: Getting the IP address
    :class: example

    If you're also using a DNS sink hole to block advertisements across the entire network (ie.
    PiHole), then resolving the hostname may fail. In this case, use the IP address for the machine
    running the MQTT broker.

    .. code-block:: shell
        :caption: How to get the IP address in Linux CLI

        hostname -I

If your broker's listener is bound to a port other than :python:`1883` (or :python:`8883` with SSL
enabled), then you need to set that port number in the MQTT binding's configuration as well.

Adding a Homie Device as an OpenHAB Thing
-----------------------------------------

First lets get a library example running on a circuitPython enabled board (with WiFi support).
See the :doc:`../examples` to understand how to run a library example. For this tutorial, we'll be
using the `Simple test <../examples.html#simple-test>`_ example.

Once you've got an example running, head over to you OpenHAB dashboard: http://openhabian:8080
(you may have to replace the hostname ``openhabian`` with the IP address like ``192.168.1.xxx``).
To see any new Homie devices discovered by the MQTT binding, navigate to "Settings" -> "Things"
(http://openhabian:8080/settings/things/). At the bottom of the screen, you should see badge-like
notification titled "Inbox".
