"""Hardware-free tests for the byte-level protocol.

Run with: pytest    (or: python -m pytest)
These validate the frames against the exact bytes observed in the Apitor app.
"""

from apitor_ble import protocol as p
from apitor_ble.protocol import Color, Direction, Motor


def test_auth_frame_robot_j():
    # Robot J password from Robot.ROBOTJ_DEVICE_PASSWORD.
    frame = p.auth_frame("j")
    assert frame.hex() == "55aa1120436e354174675a4c4a7671723863447a"
    # ...whose 16 key bytes decode to a printable ASCII string.
    assert frame[4:].decode("ascii") == "Cn5AtgZLJvqr8cDz"
    assert len(frame) == 20  # fits in a single 20-byte GATT write


def test_auth_frame_unknown_product_falls_back_to_x():
    assert p.auth_frame("zzz") == p.auth_frame("x")


def test_motor_command_matches_app_test_frame():
    # Robot.test() sends 55AA0306010A = M1, D1, speed 10.
    assert p.motor_command(Motor.M1, Direction.D1, 10).hex() == "55aa0306010a"


def test_stop_all_command():
    # stopAllMotor() -> runMotor(0x10, 0, 0).
    assert p.stop_all_command().hex() == "55aa03100000"


def test_led_command_appends_two_zero_bytes():
    # turnOnLed(index, color) -> 55AA04 index color 00 00.
    assert p.led_command(4, Color.BLUE).hex() == "55aa0404060000"


def test_byte_clamping():
    # Negative / oversized values wrap into a single byte, like the app's casts.
    assert p.motor_command(6, 1, 300).hex() == "55aa0306012c"


def test_device_name_matching():
    assert p.device_name_matches("ApitorTJ-1234", "j")
    assert p.device_name_matches("apitortj", "j")
    assert not p.device_name_matches("ApitorTS-1234", "j")
    assert not p.device_name_matches(None, "j")


def test_chunk_write_splits_at_20_bytes():
    data = bytes(range(45))
    chunks = p.chunk_write(data)
    assert [len(c) for c in chunks] == [20, 20, 5]
    assert b"".join(chunks) == data
