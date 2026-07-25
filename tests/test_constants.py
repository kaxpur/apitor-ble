"""Tests that the protocol is built from the named constants (no magic numbers)."""

from apitor_ble import constants as c
from apitor_ble import protocol as p
from apitor_ble.protocol import Color, Direction, Motor


def test_headers_are_built_from_constants():
    assert p.HEADER_MOTOR == bytes((c.FRAME_HEADER_0, c.FRAME_HEADER_1, c.CMD_MOTOR))
    assert p.HEADER_LED == bytes((c.FRAME_HEADER_0, c.FRAME_HEADER_1, c.CMD_LED))
    assert p.HEADER_SENSOR == bytes(
        (c.FRAME_HEADER_0, c.FRAME_HEADER_1, c.CMD_SENSOR, c.SENSOR_MODE)
    )


def test_enum_values_match_constants():
    assert Motor.M1 == c.MOTOR_M1
    assert Motor.STOP_ALL == c.MOTOR_STOP_ALL
    assert Direction.D1 == c.DIR_D1
    assert Color.BLUE == c.COLOR_BLUE
    assert Color.WHITE == c.COLOR_WHITE


def test_motor_frame_first_bytes_use_constants():
    frame = p.motor_command(c.MOTOR_M1, c.DIR_D1, 8)
    assert frame[0] == c.FRAME_HEADER_0
    assert frame[1] == c.FRAME_HEADER_1
    assert frame[2] == c.CMD_MOTOR


def test_gatt_uuids_shared_with_constants():
    assert p.UUID_SERVICE == c.UUID_SERVICE
    assert p.UUID_WRITE == c.UUID_WRITE
    assert p.UUID_NOTIFY == c.UUID_NOTIFY
