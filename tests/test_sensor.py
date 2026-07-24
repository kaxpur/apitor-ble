"""Hardware-free tests for notification decoding."""

from apitor_ble.sensor import FrameKind, decode_notification


def test_sensor_frame_recognized():
    f = decode_notification(bytes.fromhex("55aa0580000000000000"))
    assert f.kind is FrameKind.SENSOR
    assert f.is_sensor
    assert not f.low_power


def test_sensor_low_power_flag():
    # Byte index 7 == 2 signals low battery (Robot.onMessage).
    raw = bytearray(10)
    raw[0:4] = bytes.fromhex("55aa0580")
    raw[7] = 0x02
    f = decode_notification(bytes(raw))
    assert f.low_power is True


def test_sensor_payload_strips_header():
    f = decode_notification(bytes.fromhex("55aa0580aabbccdd"))
    assert f.payload.hex() == "aabbccdd"


def test_unknown_frame_is_preserved_not_raised():
    f = decode_notification(bytes.fromhex("deadbeef"))
    assert f.kind is FrameKind.UNKNOWN
    assert f.hex == "deadbeef"
    assert not f.low_power


def test_short_frame_does_not_crash():
    f = decode_notification(b"")
    assert f.kind is FrameKind.UNKNOWN
    assert f.low_power is False


def test_wheels_frame_decode():
    # indices: 0-2 header(55 aa 03), 4=dist, 5=lowpwr, 6=buf, 8=end-flag
    raw = bytes.fromhex("55aa03" + "00" + "05" + "00" + "02" + "00" + "00")
    assert len(raw) == 9
    f = decode_notification(raw)
    assert f.kind is FrameKind.WHEELS
    assert f.wheel_distance == 5
    assert f.order_buffer_size == 2
    assert f.order_action_end is True  # byte[8] == 0
