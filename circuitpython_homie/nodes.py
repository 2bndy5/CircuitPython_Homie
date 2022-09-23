"""This module holds the Homie implementation for a device's node(s)."""
try:
    from typing import TYPE_CHECKING, List

    if TYPE_CHECKING:  # avoids cyclical imports
        from .properties import HomieProperty
except ImportError:
    pass  # don't type check on CircuitPython firmware

from .helpers import validate_id


class HomieNode:  # pylint: disable=too-few-public-methods
    """A class to represent a Homie device's individual node.

    :param name: The human friendly name of the node.
    :param node_type: A description of the node's type.
    :param node_id: A unique identifying `str` to use in the generated MQTT topic.
        If this parameter is not specified, then the ``name`` parameter will be used
        (providing it conforms to Homie specifications - see `validate_id()`).
    """

    def __init__(
        self, name: str, node_type: str, node_id: str = None, **extra_attributes
    ):
        #: The node's human friendly ``$name``  attribute.
        self.name = name
        #: The node's ``$type`` attribute.
        self.type = node_type
        #: The node's ID as used in the generated MQTT topic.
        self.node_id = validate_id(name if not node_id else node_id)
        #: The node's properties is a list of `HomieProperty` objects.
        self.properties = []  # type: List[HomieProperty]
        for attr_name, attr_val in extra_attributes.items():
            setattr(self, attr_name, attr_val)
