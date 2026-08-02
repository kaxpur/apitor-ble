"""Tests for ApitorRobot that don't need hardware or a live connection."""

import pytest

from apitor_ble.robot import ApitorRobot


def test_address_property_reflects_constructor():
    r = ApitorRobot(address="EB:28:75:C0:66:07", product="j")
    assert r.address == "EB:28:75:C0:66:07"
    assert r.is_connected is False


def test_requires_address_or_device():
    with pytest.raises(ValueError):
        ApitorRobot()
