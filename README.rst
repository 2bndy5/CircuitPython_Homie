Introduction
============


.. image:: https://readthedocs.org/projects/circuitpython-homie/badge/?version=latest
    :target: https://circuitpython-homie.rtfd.io/
    :alt: Documentation Status
.. image:: https://github.com/2bndy5/CircuitPython_Homie/workflows/Build%20CI/badge.svg
    :target: https://github.com/2bndy5/CircuitPython_Homie/actions
    :alt: Build Status
.. image:: https://codecov.io/gh/2bndy5/CircuitPython_Homie/branch/main/graph/badge.svg?token=FOEW7PBQG8
    :target: https://codecov.io/gh/2bndy5/CircuitPython_Homie
    :alt: Test Code Coverage
.. image:: https://static.pepy.tech/personalized-badge/circuitpython-homie?period=total&units=international_system&left_color=grey&right_color=blue&left_text=PyPI%20Downloads
    :target: https://pepy.tech/project/circuitpython-homie

Homie v4 specifications for MQTT implemented in CircuitPython

.. image:: https://homieiot.github.io/img/works-with-homie.svg
    :alt: Works with MQTT Homie
    :target: https://homieiot.github.io/

Dependencies
------------

This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_
* `Adafruit MiniMQTT Library <https://docs.circuitpython.org/projects/minimqtt/en/latest/>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://circuitpython.org/libraries>`_
or individual libraries can be installed using `circup <https://github.com/adafruit/circup>`_.

Installing from PyPI
--------------------

.. code-block:: shell

    pip install circuitpython-homie

On supported GNU/Linux systems like the Raspberry Pi, you can install the driver locally `from
PyPI <https://pypi.org/project/circuitpython-homie/>`_.
To install for current user:

.. code-block:: shell

    pip3 install circuitpython-homie

To install system-wide (this may be required in some cases):

.. code-block:: shell

    sudo pip3 install circuitpython-homie

To install in a virtual environment in your current project:

.. code-block:: shell

    mkdir project-name && cd project-name
    python3 -m venv .env
    source .env/bin/activate
    pip3 install circuitpython-homie

Installing to a Connected CircuitPython Device with Circup
**********************************************************

Make sure that you have ``circup`` installed in your Python environment.
Install it with the following command if necessary:

.. code-block:: shell

    pip3 install circup

With ``circup`` installed and your CircuitPython device connected use the
following command to install:

.. code-block:: shell

    circup install homie

Or the following command to update an existing version:

.. code-block:: shell

    circup update

Usage Examples
--------------

Using the examples requires a secrets.py file that stores your secret information about the MQTT
broker and network settings. This is `described with detail in the documentation
<https://circuitpython-homie.rtfd.io/en/latest/examples.html>`_.

See the examples in the
`examples <https://github.com/2bndy5/CircuitPython_Homie/tree/main/examples>`_ folder.
These will be included with the Circuitpython Community bundle as well.

Documentation
-------------

.. _Contributing Guidelines: https://circuitpython-homie.rtfd.io/en/latest/contributing.html

API documentation for this library can be found on
`Read the Docs <https://circuitpython-homie.rtfd.io/>`_.

Instructions for build the documentation is in our `Contributing Guidelines`_.

Contributing
------------

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/2bndy5/CircuitPython_Homie/blob/HEAD/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.

See also our `Contributing Guidelines`_ for information about the development workflow.
