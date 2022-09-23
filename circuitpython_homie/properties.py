"""This modules holds the Homie implementations for a node's properties."""
from .helpers import validate_id


class HomieProperty:
    """A class to represent a single property of a Homie device's node.

    .. tip:: The current value of an instantiated property can be fetched by calling the
        object directly.

        .. code-block:: python

            led_property = HomieProperty("color", "color", init_value="0,255,0")
            color = led_property()  # pass no arguments

    :param name: The human friendly name of the node.
    :param data_type: The node's data type.
    :param property_id: A unique identifying `str` to use in the generated MQTT topic.
        If this parameter is not specified, then the ``name`` parameter will be used
        (providing it conforms to Homie specifications - see `validate_id()`).
    :param init_value: The property's initial value.
    """

    def __init__(
        self,
        name: str,
        data_type: str,
        property_id: str = None,
        init_value="",
        **extra_attributes
    ):
        #: The property's human friendly ``$name`` attribute
        self.name = name
        #: The property's ``$datatype`` attribute
        self.datatype = data_type
        #: The property's value.
        self._value = init_value
        #: The property's ID as used in the generated MQTT topic.
        self.property_id = validate_id(name if not property_id else property_id)
        for attr_name, attr_val in extra_attributes.items():
            setattr(self, attr_name, attr_val)
        self._callback = None

    def __call__(self):
        """Make instance objects callable to get the property's value."""
        return self._value

    def __repr__(self):
        """return a human friendly representation of this property."""
        return "<HomieProperty {} ({}) type {}>".format(
            self.name, self.property_id, self.datatype
        )

    def set(self, value):
        """Change the property's value.

        :param value: The new value to be used as the property's value.

        .. important::
            This function will not update the value on the MQTT broker.
            Instead use `HomieDevice.set_property()` to do that.
        """
        self._value = value

    def is_settable(self) -> bool:
        """Can this property be manipulated from the broker?"""
        if hasattr(self, "settable"):
            return getattr(self, "settable")
        return False

    @property
    def callback(self):
        """This attribute is designed to hold a pointer to a callback function that
        will be used when the property's value changes."""
        if self.is_settable() and callable(self._callback):
            return self._callback
        raise NotImplementedError("{} property is not `settable`.".format(self.name))

    @callback.setter
    def callback(self, method):
        if not callable(method):
            raise ValueError("The given parameter is not a method.")
        self._callback = method
