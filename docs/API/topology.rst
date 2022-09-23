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
            label="<f0> Node | <f1> attributes | <f2> properties"
            shape="record"
        ]
        node2 [
            label="<f0> Node | <f1> attributes | <f2> properties"
            shape="record"
        ]
        property1 [
            label = "<f0> Property | <f1> attributes"
            shape = "record"
        ]
        property2 [
            label = "<f0> Property | <f1> attributes"
            shape = "record"
        ]
        property3 [
            label = "<f0> Property | <f1> attributes"
            shape = "record"
        ]
        property4 [
            label = "<f0> Property | <f1> attributes"
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
and humidity data from a DHT sensor to your MQTT broker for use in OpenHab. Just for fun, we'll
let OpenHab control your on-board RGB LED too. Structurally this would be organized like, so:

.. graphviz::
    :align: center

    digraph g {
        rankdir="LR"
        HomieDevice [
            label="<f0> esp32-device | <f1> attributes | <f2> nodes"
            shape="record"
        ]
        DHT [
            label="<f0> dht-node | <f1> attributes | <f2> properties"
            shape="record"
        ]
        LED [
            label="<f0> led-node | <f1> attributes | <f2> properties"
            shape="record"
        ]
        Temp [
            label = "<f0> temperate | <f1> attributes"
            shape = "record"
        ]
        Humid [
            label = "<f0> humidity | <f1> attributes"
            shape = "record"
        ]
        Color [
            label = "<f0> color | <f1> attributes"
            shape = "record"
        ]
        HomieDevice:f2 -> DHT:f0
        HomieDevice:f2 -> LED:f0
        DHT:f2 -> Temp:f0
        DHT:f2 -> Humid:f0
        LED:f2 -> Color:f0
    }
