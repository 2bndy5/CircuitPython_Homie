Tutorials
=========

To aid with user setup, this documentation is complete with tutorials about

.. toctree::
    :maxdepth: 1

    mosquitto
    openhab

.. _systemctl:

Controlling a system service in Linux (``systemctl``)
-----------------------------------------------------

These are some common commands  for ``systemctl`` on Linux that may be helpful, all of which
should require root permission (``sudo``) to execute successfully.

.. program:: systemctl

.. option:: enable

    This command is used to make a service start when the machine boots up. To enable Mosquitto
    broker (as a system service) to start on boot up:

    .. code-block:: shell

        sudo systemctl enable mosquitto

.. option:: status

    This command is used to print the status of a running mosquitto broker. It can be useful because
    it will show if there was any errors in running the process.

    .. code-block:: shell

        sudo systemctl status mosquitto

    .. hint::
        If there were any errors, then this will tell you what file in which the logs were saved.

.. option:: restart

    This command is useful if you need to restart your broker after making changes to the
    configuration.

    .. code-block:: shell

        sudo systemctl restart mosquitto

.. option:: start

    The command to start the broker as a service (as opposed to directly running the ``mosquitto``
    or ``openhab`` binary executables). This is really only useful if you don't want the broker
    service to start on boot (ie. doing tests configurations).

    .. code-block:: shell

        sudo systemctl start openhab

.. option:: stop

    The command to stop any running system service. This is mentioned for completeness
    because it is the opposite of :std:option:`start`.
