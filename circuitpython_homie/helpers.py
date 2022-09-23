"""This module holds some helpers used in various other modules."""
import re

DEVICE_STATES = [
    "init",
    "ready",
    "disconnected",
    "sleeping",
    "alert",
    "lost",
]
"""A list of valid device states according to the
`Homie specification's Life Cycle
<https://homieiot.github.io/specification/#device-lifecycle>`_."""


def validate_id(_id: str) -> str:
    """Conform and validate a given ID to Homie specifications.

    :param _id: The given ID.

        .. note::
            This function strips ``-`` characters from the beginning and ending
            of the ID. A leading ``$`` is also removed since that character is
            reserved for Homie attributes.
    :returns: A valid ID from the value passed to the ``_id`` parameter.
    :throws: If the given ID contains anything other than
        lowercase letters (a-z), numbers (0-9), or hyphens (``-``), then
        this function will raise a `ValueError` exception.
    """
    _id = _id.rstrip("-").lstrip("$-").lower()
    if re.match("^[a-z0-9\\-]+$", _id) is None:
        raise ValueError(
            "Device ID can only consist of lowercase a-z, digits 0-9, or hyphens."
        )
    return _id
