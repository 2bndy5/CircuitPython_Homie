Recipes
========

.. automodule:: circuitpython_homie.recipes

    Colors
    -------

    .. autoclass:: PropertyRGB
        :members:
    .. autoclass:: PropertyHSV
        :members:

    Boolean
    -------

    .. autoclass:: PropertyBool
        :members: validate
        :show-inheritance:

    Numbers
    -------

    .. autoclass:: PropertyPercent
        :members: validate
    .. autoclass:: PropertyInt
        :members: validate
    .. autoclass:: PropertyFloat
        :members: validate

    Time
    ----

    .. autoclass:: PropertyDateTime
        :members: convert
        :show-inheritance:
    .. autoclass:: PropertyDuration
        :members: convert
        :show-inheritance:

Helpers
-------

These module attributes help validation of certain values.

.. autofunction:: circuitpython_homie.validate_id
.. autodata:: circuitpython_homie.DEVICE_STATES
.. autodata:: circuitpython_homie.PAYLOAD_TYPES
