Introduction
============


.. image:: https://readthedocs.org/projects/circuitpython-homie/badge/?version=latest
    :target: https://circuitpython-homie.readthedocs.io/
    :alt: Documentation Status
.. image:: https://github.com/2bndy5/CircuitPython_Homie/workflows/Build%20CI/badge.svg
    :target: https://github.com/2bndy5/CircuitPython_Homie/actions
    :alt: Build Status
.. image:: https://codecov.io/gh/2bndy5/CircuitPython_Homie/branch/main/graph/badge.svg?token=FOEW7PBQG8
    :target: https://codecov.io/gh/2bndy5/CircuitPython_Homie
    :alt: Test Code Coverage

Homie specifications for MQTT implemented in CircuitPython

.. image:: https://homieiot.github.io/img/works-with-homie.svg
    :alt: Works with MQTT Homie
    :target: https://homieiot.github.io/
    :width: 50%

Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://circuitpython.org/libraries>`_
or individual libraries can be installed using
`circup <https://github.com/adafruit/circup>`_.

Installing from PyPI
=====================

.. note::
    This library is not available on PyPI yet. Install documentation is included
    as a standard element. Stay tuned for PyPI availability!

.. admonition:: todo

    Remove the above note if PyPI version is/will be available at time of release.

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
    python3 -m venv .venv
    source .env/bin/activate
    pip3 install circuitpython-homie

Installing to a Connected CircuitPython Device with Circup
==========================================================

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

Usage Example
=============

.. admonition:: todo

    Add a quick, simple example. It and other examples should live in the
    examples folder and be included in docs/examples.rst.

Documentation
=============
API documentation for this library can be found on `Read the Docs <https://circuitpython-homie.readthedocs.io/>`_.

For information on building library documentation, please check out
`this guide <https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1>`_.

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/2bndy5/CircuitPython_Homie/blob/HEAD/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.
