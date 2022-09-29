"""Tests for the generic HomieProperty class."""
from typing import Callable, Optional, cast
import pytest
from circuitpython_homie import HomieProperty, validate_id


@pytest.mark.parametrize(
    "_id", [None, "unique-ID", pytest.param("Bad ID", marks=pytest.mark.xfail)]
)
@pytest.mark.parametrize(
    "settable", [None, False, True, pytest.param(1, marks=pytest.mark.xfail)]
)
@pytest.mark.parametrize(
    "retained", [None, False, True, pytest.param(0, marks=pytest.mark.xfail)]
)
@pytest.mark.parametrize(
    "datatype", ["string", pytest.param("X", marks=pytest.mark.xfail)]
)
def test_attrs(datatype: str, _id: str, settable: bool, retained: bool):
    """Test a generic property for ID validation and settable/retained attributes."""
    attrs = dict(property_id=_id)
    if settable is not None:
        attrs["settable"] = settable
    if retained is not None:
        attrs["retained"] = retained
    prop = HomieProperty("name", datatype, **attrs)
    assert str(prop) == ("name" if _id is None else validate_id(_id))
    if settable is None:
        assert prop.is_settable() is False
    else:
        assert prop.is_settable() is settable
    if retained is None:
        assert prop.is_retained() is True
    else:
        assert prop.is_retained() is retained


def call(*_):
    """A method to use as a callback for tests."""
    return True


@pytest.mark.parametrize("method", [call, pytest.param(None, marks=pytest.mark.xfail)])
@pytest.mark.parametrize(
    "settable", [True, pytest.param(False, marks=pytest.mark.xfail)]
)
def test_callback(method: Optional[Callable], settable: Optional[bool]):
    """Test the property's `callback` attribute."""
    prop = HomieProperty("test", settable=settable)
    if settable is True:
        error_raised = False
        try:
            _ = prop.callback
        except NotImplementedError:
            error_raised = True
        finally:
            if not error_raised:
                raise RuntimeError(
                    "expected a NotImplementedError, but didn't catch it"
                )
    prop.callback = method
    assert cast(Optional[Callable], prop.callback)()
