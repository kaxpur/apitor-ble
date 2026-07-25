"""Tests for the exception hierarchy."""

import pytest

from apitor_ble.exceptions import (
    ApitorError,
    AuthorizationError,
    ConnectionError,
    DiscoveryError,
    ProtocolError,
)
from apitor_ble.protocol import chunk_write


@pytest.mark.parametrize(
    "exc",
    [DiscoveryError, ConnectionError, AuthorizationError, ProtocolError],
)
def test_all_derive_from_apitor_error(exc):
    assert issubclass(exc, ApitorError)


def test_apitor_error_is_runtime_error_for_back_compat():
    assert issubclass(ApitorError, RuntimeError)


def test_base_catches_specific():
    with pytest.raises(ApitorError):
        raise DiscoveryError("nothing found")


def test_chunk_write_raises_protocol_error_on_bad_size():
    with pytest.raises(ProtocolError):
        chunk_write(b"abc", size=0)


def test_robot_reexports_apitor_error():
    # Older code imported ApitorError from apitor_ble.robot.
    from apitor_ble.robot import ApitorError as RobotApitorError

    assert RobotApitorError is ApitorError
