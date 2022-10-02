
.. role:: oh-red(literal)
    :class: oh-red oh
.. role:: oh-green(literal)
    :class: oh-green oh
.. role:: oh-blue(literal)
    :class: oh-blue oh

Using Homie with OpenHAB_
=========================

OpenHAB_ is a Java based software that can be used on a computer connected to your Local Area
Network (LAN) to monitor (or control) various "smart devices" in your home (or building).
Typically, it is meant to be installed to a headless machine like a Raspberry Pi, but any
computer you have sitting around should work. The machine needs to always be running and
connected to your LAN.

Prerequisite
------------

1. Install OpenHAB_ using their
   `excellent download instructions <https://www.openhab.org/download/>`_.

   .. seealso::
       If you install OpenHAB using ``apt`` packages, then the section about :ref:`systemctl`
       may be beneficial.
2. :doc:`mosquitto` and configure it to use your LAN.

.. hint::
    You can use the same machine to host the MQTT broker and the OpenHAB server. Usually people
    use a Raspberry Pi to do this.

.. _OpenHAB Getting Started instructions: https://www.openhab.org/docs/tutorial/first_steps.html

I highly recommend following the `OpenHAB Getting Started instructions`_ to get a feel for using
the interface. The rest of this tutorial will assume that you are logged into the OpenHAB interface
with an OpenHAB administrator account. This should have been covered in the
`OpenHAB Getting Started instructions`_

.. _MQTT binding: https://www.openhab.org/addons/bindings/mqtt/
.. _MQTT Homie binding: https://www.openhab.org/addons/bindings/mqtt.homie/
.. |click| replace:: Click or tap

.. tip::
  Some of the images here are hyperlinked to the http://openhabian:8080 domain for quicker access.
  If you are using a different hostname or a static IP address, then you can adjust the address in
  your browser's address bar.

Installing the `MQTT binding`_
------------------------------

Building off `OpenHAB's "Add a Thing - Simple (Install the Binding)" instructions
<https://www.openhab.org/docs/tutorial/things_simple.html#install-the-binding>`_, look for a
`MQTT binding`_ in the `"bindings add-ons" list <http://openhabian:8080/settings/addons/>`_.
|click| the :homie-val:`show <n> more` button at the bottom of the OpenHAB Distribution list if
you don't see the `MQTT binding`_.

.. admonition:: Notice
    :class: example

    The `MQTT binding`_ is one of the official OpenHAB addons. It is not a Community addon.

.. image:: ../_static/tutorial_images/mqtt_binding-light.png
    :class: only-light align-center
    :target: http://openhabian:8080/settings/addons/binding-mqtt
.. image:: ../_static/tutorial_images/mqtt_binding-dark.png
    :class: only-dark align-center
    :target: http://openhabian:8080/settings/addons/binding-mqtt

|click| the :homie-val:`install` button to install the binding and add MQTT capability to your
OpenHAB server.

.. md-admonition::
    :class: info

    `Installing the MQTT binding`_ in OpenHAB will also install Homie support automatically. More info
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

.. |OH-thing| replace:: OpenHAB Thing

.. _add_broker_as_thing:

Adding the MQTT broker as an |OH-thing|
***************************************

After `Installing the MQTT binding`_, navigate back to the settings page and open
`the "Things" category <http://openhabian:8080/settings/things/>`_. You may think that installing
the MQTT binding didn't change anything, but automatic discovery of MQTT-capable devices still
requires an |OH-thing| to represent the MQTT broker.

.. |OH_plus| replace:: :oh-blue:`+`
.. _OH_plus: http://openhabian:8080/settings/things/add

1. |click| the floating |OH_plus|_ button at
   the bottom of the page.
2. You should see a list of the installed bindings to choose from. |click| on the MQTT binding.

   .. image:: ../_static/tutorial_images/mqtt_binding_thing-light.png
       :class: only-light align-center
       :target: http://openhabian:8080/settings/things/mqtt
   .. image:: ../_static/tutorial_images/mqtt_binding_thing-dark.png
       :class: only-dark align-center
       :target: http://openhabian:8080/settings/things/mqtt
3. At the top of the list of options that you can add as |OH-thing|\ s, you should see the MQTT broker option.
   It will have a badge on it that says :oh-blue:`Bridge`. |click| on the MQTT broker option.

   .. image:: ../_static/tutorial_images/mqtt_broker_thing-light.png
       :class: only-light align-center
   .. image:: ../_static/tutorial_images/mqtt_broker_thing-dark.png
       :class: only-dark align-center
4. Enter the hostname or IP address of the machine that is running the MQTT broker.

   Typically, the same machine can be used for serving OpenHAB and the MQTT broker. If you're using
   the openhabian OS installed on a Raspberry Pi, then the hostname will be ``openhabian``.

   .. details:: Getting the IP address
       :class: example

       If you're also using a DNS sink hole to block advertisements across the entire network (ie.
       PiHole), then resolving the hostname may fail. In this case, use the IP address for the machine
       running the MQTT broker.

       .. code-block:: shell
           :caption: How to get the IP address in Linux CLI

           hostname -I

   :Advanced Options:
       The following settings are only shown in the advanced options:

       - ``Username`` and ``Password`` (in case you followed the steps to
         :ref:`mqtt_user_password`)

         .. note::
             The ``Username`` and ``Password`` fields are not related to the OpenHAB user
             account. Actually, these are the values used when :ref:`mqtt_user_password`.

             Your internet browser may suggest otherwise if your OpenHAB account credentials are
             saved in the browser's settings.
       - the ``Port`` number (in case you are not using the default :python:`1883` or
         :python:`8883` with SSL/TLS enabled)

       The advanced options are only shown if the "Show advanced" checkbox at the top of the list
       is checked.
5. |click| on the :oh-blue:`Create Thing` button at the bottom of the page when done entering the MQTT
   broker criteria. Now in your `OpenHAB list of Things <http://openhabian:8080/settings/things/>`_,
   you should see the status of the MQTT broker.

   .. image:: ../_static/tutorial_images/mqtt_broker_thing_status-light.png
       :class: only-light align-center
   .. image:: ../_static/tutorial_images/mqtt_broker_thing_status-dark.png
       :class: only-dark align-center

   If you see a badge that says :oh-red:`ERROR:COMM` (where it should say :oh-green:`ONLINE`), it
   means that there's something wrong with the values you entered in step 4. |click| on the MQTT
   broker Thing to change the settings accordingly. **Don't forget** to hit ``save`` at the top of
   the page after making the necessary changes.

   .. hint::
       Hover your mouse (or tap and hold) over the :oh-red:`ERROR` badge to see a tooltip briefly
       explaining the reason for the error.

Adding a Homie Device as an |OH-thing|
-----------------------------------------

Once you have finished :ref:`add_broker_as_thing`, you are now ready to start using OpenHAB's automatic
discovery of Homie Devices. This section should be repeated for any instantiated `HomieDevice`
object.

.. note::
  Once completed, there is no need to repeat these steps again for the same `HomieDevice` object
  unless you have changed the ``device_id`` parameter to the `HomieDevice` constructor. Connecting
  & disconnecting a Homie Device that are already added as |OH-thing|\ s should be automatically
  handled by the OpenHAB  `MQTT Homie binding`_.

First lets get a library example running on a circuitPython enabled board (with WiFi support).
See the :doc:`../examples` to understand how to run a library example. For this tutorial, we'll be
using the `Simple test <../examples.html#simple-test>`_ example.

Once you've got an example running, head over to you OpenHAB dashboard: http://openhabian:8080
(you may have to replace the hostname ``openhabian`` with the IP address like ``192.168.1.xxx``).
To see any new Homie devices discovered by the MQTT binding, navigate to "Settings" -> "Things"
(http://openhabian:8080/settings/things/). At the bottom of the screen, you should see badge-like
notification titled "Inbox".
