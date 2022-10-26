Setting Up an MQTT broker (Mosquitto)
=====================================

`Mosquitto <https://mosquitto.org/>`_ is a popular choice and is available for most platforms.
`Download/install instructions <https://mosquitto.org/download/>`_ are pretty straight forward.

.. admonition:: Installing Mosquitto on Linux
    :class: todo

    .. code-block:: shell

        sudo apt-get install mosquitto

Configuring Mosquitto
---------------------

You may have to change the default configuration used by the Mosquitto broker to allow other
network devices to connect. For me (using v2.0.11 on Ubuntu), this meant editing the file
located at **/etc/mosquitto/mosquitto.conf**.

Open the file with root permission from the terminal (or via SSH client):

.. code-block:: shell

    sudo nano /etc/mosquitto/mosquitto.conf

Make sure a ``listener`` is bound to a port (typically ``1883`` by default) with the domain
``0.0.0.0`` (the server machine's ``localhost``). If you want to skip
mqtt_user_password_, then add a line that sets ``allow_anonymous`` to ``true``.
It should end up looking like this:

.. code-block:: pacmanconf
    :caption: /etc/mosquitto/mosquitto.conf

    listener 1883 0.0.0.0

    # to bypass username and password configuration
    allow_anonymous true

Save and close the file, then :std:option:`systemctl restart` the broker.

Checking the Mosquitto broker logs
**********************************

By default, the logs for mosquitto are saved to **/var/log/mosquitto/mosquitto.log**. This can be
changed with the ``log_dest file`` value in the configuration:

.. code-block:: text
    :caption: Default Log Destination in **/etc/mosquitto/mosquitto.conf**

    log_dest file /var/log/mosquitto/mosquitto.log

If the broker fails to understand a given configuration, then these logs will point to what
configuration option was erroneous.

.. code-block:: shell
    :caption: Print Logs in the terminal (requires root permission)

    sudo cat /var/log/mosquitto/mosquitto.log

.. _mqtt_user_password:

Setting a username and password
-------------------------------

It is recommended that your MQTT broker's access be secured via a username and password.
The Mosquitto broker uses a password file to store these values securely.

1. .. code-block:: shell
       :caption: Create the password file for a user

       mosquitto_passwd -c pswd.txt username

   The above command creates a password file named ``pswd.txt`` for a user named ``username``.

   .. details:: Adding another user
       :class: check

       Use the ``-b`` switch to add more users:

       .. code-block:: shell

           mosquitto_passwd -b pswd.txt other_username user_password
   .. details:: Removing a user
       :class: fail

       Use the ``-D`` switch to remove a user:

       .. code-block:: shell

           mosquitto_passwd -D pswd.txt other_username user_password
   .. note::
       If you inspect the password file  after creation, you will notice that the password
       associated with usernames is not what you entered. This is because ``mosquitto_passwd``
       encrypts the password using a SHA512 scheme.
2. .. code-block:: shell
       :caption: Move the password file to the broker's configuration path

       sudo mv pswd.txt /etc/mosquitto/

   The **pswd.txt** file you created should now be next to you broker's configuration file
   (**/etc/mosquitto/mosquitto.conf**).
3. Add the following lines to the broker's configuration file.

   .. details:: Open your broker's configuration file
       :class: faq

       .. code-block:: shell

           sudo nano /etc/mosquitto/mosquitto.conf

   .. code-block:: text
       :caption: add the password file's path to the configuration

       per_listener_settings true

       listener 1883 0.0.0.0
       allow_anonymous false
       password_file /etc/mosquitto/pswd.txt

   - ``per_listener_settings`` is required to assign the password file to a listener.
   - ``alow_anonymous`` should be disabled if you want to prohibit non-authenticated access to
     your broker.
   - ``password_file`` is the path to the password file created with encrypted passwords.

4. :std:option:`systemctl restart` (or :std:option:`systemctl start`) to force the broker to use
   the updated configuration.

Enabling SSL/TLS support
------------------------

If desired, you can enable SSL/TLS support in your broker for additional security and
anti-corruption of data. Since this is all rather technical and a bit more involved, I would
recommend following `Steve's Internet Guide <http://www.steves-internet-guide.com/mosquitto-tls/>`_.

MQTT Explorer
-------------

To verify that this library is publishing and subscribing topics with your MQTT broker, I
recommend using the `MQTT Explorer app <https://mqtt-explorer.com/>`_ (which works well
on my Windows PC).
`Downloads are available <https://github.com/thomasnordquist/MQTT-Explorer/releases/latest>`_
for most platforms. There's even a stable release deployed in the Windows App Store and the
Snap Store for Linux.
