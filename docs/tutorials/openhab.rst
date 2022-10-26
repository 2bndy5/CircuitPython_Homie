
.. role:: oh-red(literal)
    :class: oh-red oh
.. role:: oh-green(literal)
    :class: oh-green oh
.. role:: oh-blue(literal)
    :class: oh-blue oh
.. role:: oh-orange(literal)
    :class: oh-orange oh

.. _MQTT binding: https://www.openhab.org/addons/bindings/mqtt/
.. _MQTT Homie binding: https://www.openhab.org/addons/bindings/mqtt.homie/
.. _Simple test: ../examples.html#simple-test
.. |click| replace:: Click or tap
.. |oh-thing| replace:: OpenHAB Thing
.. |oh-item| replace:: OpenHAB Item
.. |homie-dev| replace:: Homie Device

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

.. note::

    The `MQTT binding`_ is one of the official OpenHAB addons. It is not a Community addon.

.. image:: ../_static/tutorial_images/mqtt_binding-light.png
    :class: only-light align-center
    :target: http://openhabian:8080/settings/addons/binding-mqtt
.. image:: ../_static/tutorial_images/mqtt_binding-dark.png
    :class: only-dark align-center
    :target: http://openhabian:8080/settings/addons/binding-mqtt

|click| the :homie-val:`install` button to install the binding and add MQTT capability to your
OpenHAB server.

`Installing the MQTT binding`_ in OpenHAB will also install Homie support automatically. More info
about Homie support can be found at the `MQTT Homie binding`_ page.

.. admonition:: Homie v3 vs Homie v4
    :class: missing
    :name: v3-vs-v4

    The OpenHAB `MQTT Homie binding`_ will say that it supports Homie v3.x specifications. This library
    implements Homie v4 specifications. Homie v4 is mostly backward compatible with Homie v3 with
    the following exceptions:

    - `Node Arrays <https://homieiot.github.io/specification/spec-core-v3_0_1/#arrays>`_
      are not supported in Homie v4. Incidentally, Arrays aren't implemented in OpenHAB's
      `MQTT Homie binding`_ because the Homie specification was too vague which is why it was
      removed in Homie v4 (see `this HomieIoT thread comment
      <https://github.com/homieiot/convention/issues/90#issuecomment-385425001>`_).
    - `Device Statistics <https://homieiot.github.io/specification/spec-core-v3_0_1/#device-statistics>`_
      are not supported in Homie v4. This was removed in Homie v4 in favor of using nodes' properties
      (see `this HomieIoT discussion <https://github.com/homieiot/convention/issues/102>`_).

    These missing features are memory and process intensive for microcontrollers. At this time,
    there is no plan to add Homie v3 support for this library.

.. _add_broker_as_thing:

Adding the MQTT broker as an |oh-thing|
***************************************

After `Installing the MQTT binding`_, navigate back to the settings page and open
`the "Things" category <http://openhabian:8080/settings/things/>`_. You may think that installing
the MQTT binding didn't change anything, but automatic discovery of MQTT-capable devices still
requires an |oh-thing| to represent the MQTT broker.

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
3. At the top of the list of options that you can add as |oh-thing|\ s, you should see the MQTT broker option.
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

Adding a |homie-dev| as an |oh-thing|
-----------------------------------------

Once you have finished :ref:`add_broker_as_thing`, you are now ready to start using OpenHAB's automatic
discovery of |homie-dev|\ s. This section should be repeated for any instantiated `HomieDevice`
object.

.. admonition:: Only do this once
    :class: check

    Once completed, there is no need to repeat these steps again for the same `HomieDevice` object
    unless you have changed the ``device_id`` parameter to the `HomieDevice` constructor. Connecting
    & disconnecting a |homie-dev| that are already added as |oh-thing|\ s should be automatically
    handled by the OpenHAB  `MQTT Homie binding`_.

First lets get a library example running on a circuitPython enabled board (with WiFi support).
See the :doc:`../examples` to understand how to run a library example. For this tutorial, we'll be
using the `Simple test`_ example.

Once you've got an example running on your circuitpython board, The `HomieDevice` must be added to
OpenHAB as an |oh-thing|. The `HomieProperty` values are used in OpenHAB as a |oh-item|, and each
|oh-item| must be "linked" to an |oh-thing|'s "channel"

1. To see any new Homie devices discovered by the MQTT binding, navigate to
   `Settings -> Things <http://openhabian:8080/settings/things/>`_. |click| on the notification
   titled :oh-red:`Inbox` at the bottom of the screen.
2. You should see your new `HomieDevice` listed by it's ``device-_id`` (a required parameter in the
   `HomieDevice` constructor).

   .. image:: ../_static/tutorial_images/discovered_thing-light.png
       :class: only-light align-center
   .. image:: ../_static/tutorial_images/discovered_thing-dark.png
       :class: only-dark align-center

   |click| on the discovered |homie-dev| and select :homie-dev:`Add as Thing` from the pop-up menu.
   It will ask you for a customized name to be assigned to the |oh-thing|. By default it will use
   the ``device_id`` if not changed, so this step is optional. |click| the :oh-orange:`OK` button
   when done.
3. You should now see the |homie-dev| in your list of |oh-thing|\ s.

   .. image:: ../_static/tutorial_images/homie_thing-light.png
       :class: only-light align-center
   .. image:: ../_static/tutorial_images/homie_thing-dark.png
       :class: only-dark align-center

   To use this |homie-dev|'s properties in the OpenHAB user interfaces, you need to create an
   |oh-item| for each |homie-dev| property (programmatically instantiated with `HomieProperty` or
   :doc:`one of its derivatives <../API/recipes>`). Each |oh-item| must be linked to a |homie-dev|
   property via an |oh-thing|'s channel(s).

   To see the channels, navigate to the configuration of the |oh-thing| that represents your
   |homie-dev| (in your list of |oh-thing|\ s). |click| on the tab named ``Channels`` at the top of
   the page.

   You should now see a list of properties belonging to your |homie-dev|. Using the `Simple test`_
   example, this list only has a ``color`` property. There are various ways to create |oh-item|\ s
   from the |oh-thing|'s ``Channels`` configuration page. Choosing 1 will depend on how you wish to
   craft your OpenHAB User Interface, Dashboard, or Sitemap.

   - |click| on an available channel and select ``Add link to Item...``, then select
     ``Create a new Item``. This will create a single |oh-item|, but the item's ID must be unique in
     OpenHAB (cannot reuse the same ID for multiple |oh-item|\ s linked to the same |oh-thing|'s
     channel). While this is the most flexible, it can also become the most tedious.
   - |click| on the button titled :homie-val:`Add points to Model`. This will create the necessary
     |oh-item|\ (s) and link them to the respective property's channel.
   - |click| on the button titled :homie-val:`Add Equipment to Model`. This is similar to
     :homie-val:`Add points to Model`, however the created |oh-item|\ (s) are put into a group that
     represents a category of equipment.

   .. admonition:: Going Forward
       :class: check

       It is important to understand `OpenHAB's Semantic Model
       <https://www.openhab.org/docs/tutorial/model.html>`_ and how they can be used when crafting
       a User Interface.

       This tutorial does not cover how to use OpenHAB in general. The main point of this tutorial
       is how to use the CircuitPython_Homie library for automatic discovery of DIY devices in
       OpenHAB.
