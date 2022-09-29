"""Tests for a HomieNode."""
import pytest
from circuitpython_homie import HomieNode, validate_id


@pytest.mark.parametrize("_id", [None, "Converted-ID"])
def test_id(_id: str):
    """Test setting of extra attributes on a `HomieNode`."""
    node = HomieNode("name", "type", node_id=_id)
    used_id = "name" if not _id else validate_id(_id)
    assert str(node) == used_id
    assert f"<HomieNode {used_id}>" == repr(node)
