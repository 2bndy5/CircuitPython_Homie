Topology
========

This library's data structures follows the
`Homie specification's topology <https://homieiot.github.io/specification/#topology>`_.
Because this implementation is written in pure python, the attributes of a Homie
device/node/property are instance attributes of the respective objects.

.. graphviz::
    :align: center

    digraph g {
        rankdir = "LR"
        device [
            label="<f0> Device | <f1> attributes | <f2> nodes"
            shape="record"
        ]
        node1 [
            label="<f0> Node1 | <f1> attributes | <f2> properties"
            shape="record"
        ]
        node2 [
            label="<f0> Node2 | <f1> attributes | <f2> properties"
            shape="record"
        ]
        property1 [
            label = "<f0> Property1 | <f1> attributes"
            shape = "record"
        ]
        property2 [
            label = "<f0> Property2 | <f1> attributes"
            shape = "record"
        ]
        property3 [
            label = "<f0> Property3 | <f1> attributes"
            shape = "record"
        ]
        property4 [
            label = "<f0> Property4 | <f1> attributes"
            shape = "record"
        ]
        device:f2 -> node1:f0
        device:f2 -> node2:f0
        node1:f2 -> property1:f0
        node1:f2 -> property2:f0
        node2:f2 -> property3:f0
        node2:f2 -> property4:f0
    }

Simple Example
--------------

Let's say you have a board equipped with an ESP32-Sx chip, and you want to broadcast temperature
and humidity data from a DHT sensor to your MQTT broker for use in OpenHAB_. Just for fun, we'll
let OpenHAB_ control your on-board RGB LED too. Structurally, this would be organized like so:

.. md-tab-set::

    .. md-tab-item:: Graphically

        .. graphviz::
            :align: center

            digraph g {
                rankdir="LR"
                "Homie Device" [
                    label="<f0> esp32-device | <f1> attributes | <f2> nodes"
                    shape="record"
                ]
                "DHT node" [
                    label="<f0> dht-node | <f1> attributes | <f2> properties"
                    shape="record"
                ]
                "LED node" [
                    label="<f0> led-node | <f1> attributes | <f2> properties"
                    shape="record"
                ]
                "Temperature property" [
                    label = "<f0> temperature | <f1> attributes"
                    shape = "record"
                ]
                "Humidity property" [
                    label = "<f0> humidity | <f1> attributes"
                    shape = "record"
                ]
                "Color property" [
                    label = "<f0> color | <f1> attributes"
                    shape = "record"
                ]
                "Homie Device":f2 -> "DHT node":f0
                "Homie Device":f2 -> "LED node":f0
                "DHT node":f2 -> "Temperature property":f0
                "DHT node":f2 -> "Humidity property":f0
                "LED node":f2 -> "Color property":f0
            }

    .. md-tab-item:: Programmatically

        .. code-block:: python

            from circuitpython_homie import HomieDevice, HomieNode
            from circuitpython_homie.recipes import PropertyFloat, PropertyRGB

            # declare device
            # let mqtt_client be the instantiated adafruit_minimqtt.MQTT object
            my_device = HomieDevice(mqtt_client, "esp32-device", "esp32-device-id")

            # declare nodes
            dht_node = HomieNode("dht-node", "sensor")
            led_node = HomieNode("led-node", "LED")

            # declare properties
            temperature_property = PropertyFloat("temperature")
            humidity_property = PropertyFloat("humidity")
            led_color_property = PropertyRGB("color", settable=True)

            # append the nodes to the device
            my_device.nodes.extend([dht_node, led_node])

            # append the properties to the appropriate nodes
            dht_node.properties.extend([temperature_property, humidity_property])
            led_node.properties.append(led_color_property)

    .. md-tab-item:: MQTT Topical Tree
        :class: topic-list

        .. details:: Legend
            :class: faq

            - ``homie`` denotes the default base topic for all Homie implementations.
              This can be changed via the `HomieDevice.base_topic` attribute.
            - :homie-dev:`topic` denotes a base topic for a device, node, or property.
            - :homie-attr:`topic` denotes a base topic for attributes that belong to a
              device, node, or property.
            - :homie-val:`value` denotes a topic's message (or value). Notice that nodes'
              base topic do not have a corresponding message.

        - ``homie``

          - :homie-dev:`esp32-device-id`

            - :homie-attr:`homie` = :homie-val:`4.0.0`
            - :homie-attr:`name` = :homie-val:`esp32-device`
            - :homie-attr:`state` = :homie-val:`ready`
            - :homie-attr:`extensions` = :homie-val:`null.dummy:none[3.x;4.x]`
            - :homie-attr:`nodes` = :homie-val:`dht-node,led-node`
            - :homie-node:`dht-node`

              - :homie-attr:`name` = :homie-val:`dht-node`
              - :homie-attr:`type` = :homie-val:`sensor`
              - :homie-attr:`properties` = :homie-val:`temperature,humidity`
              - :homie-prop:`temperature` = :homie-val:`0.0`

                - :homie-attr:`name` = :homie-val:`temperature`
                - :homie-attr:`datatype` = :homie-val:`float`
              - :homie-prop:`humidity` = :homie-val:`0.0`

                - :homie-attr:`name` = :homie-val:`humidity`
                - :homie-attr:`datatype` = :homie-val:`float`
            - :homie-node:`led-node`

              - :homie-attr:`name` = :homie-val:`led-node`
              - :homie-attr:`type` = :homie-val:`LED`
              - :homie-attr:`properties` = :homie-val:`color`
              - :homie-prop:`color` = :homie-val:`0,0,0`

                - :homie-attr:`name` = :homie-val:`color`
                - :homie-attr:`datatype` = :homie-val:`color`
                - :homie-attr:`settable` = :homie-val:`true`
