"""Tests for a `HomieDevice` object."""
import json
from pathlib import Path
from typing import Union
import pytest
from circuitpython_homie import HomieDevice, HomieProperty, HomieNode, DEVICE_STATES


def test_device(
    created_shim_dev: HomieDevice,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    """Initialize a HomieDevice object and export the
    shim client's logs for comparison."""
    monkeypatch.chdir(str(tmp_path))

    # make test results agnostic to platform and lib version
    created_shim_dev.implementation = "shim test for CircuitPython"
    created_shim_dev.fw["version"] = "dev"

    created_shim_dev.begin()  # create log of topics

    # ensure mandatory topics are published
    log_json = "fake-mqtt-log.json"
    created_shim_dev.client.export_logs()
    expected = json.loads((Path(tmp_path) / log_json).read_text(encoding="utf-8"))
    tested = json.loads((Path(__file__).parent / log_json).read_text(encoding="utf-8"))
    assert tested == expected


def test_prop_setter(created_shim_dev: HomieDevice):
    """Test `HomieDevice.set_property()`"""
    node = created_shim_dev.nodes[2]  # thermostat node
    prop = node.properties[0]  # temperature property (int)
    created_shim_dev.set_property(prop, 85)
    assert prop.value == 85


@pytest.mark.parametrize(
    "setter", [HomieProperty("dummy"), HomieNode("dummy", "dummy")]
)
@pytest.mark.xfail
def test_prop_setter_fail(
    created_shim_dev: HomieDevice, setter: Union[HomieProperty, HomieNode]
):
    """Test exceptions raised from invalid arg to set_property()"""
    created_shim_dev.set_property(setter, "false")


@pytest.mark.parametrize(
    "state", DEVICE_STATES + [pytest.param("invalid", marks=pytest.mark.xfail)]
)
def test_state_setter(created_shim_dev: HomieDevice, state: str):
    """Test `HomieDevice.set_state()`"""
    created_shim_dev.set_state(state)
