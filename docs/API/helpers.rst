Recipes
========

.. automodule:: circuitpython_homie.recipes

    Boolean
    -------

    .. autoclass:: PropertyBool
        :members: validate
        :show-inheritance:

    Percent
    -------

    .. autoclass:: PropertyPercent
        :members: validate
        :show-inheritance:

    Color
    -------

    .. autoclass:: PropertyRGB
        :members:
    .. autoclass:: PropertyHSV
        :members:

    Time
    ----

    .. autoclass:: PropertyDateTime
        :members: convert
        :show-inheritance:

Helpers
-------

These module attributes help validation of certain values.

.. autofunction:: circuitpython_homie.validate_id
.. autodata:: circuitpython_homie.DEVICE_STATES
.. autodata:: circuitpython_homie.PAYLOAD_TYPES
