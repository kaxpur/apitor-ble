"""Tests for the per-robot driving profiles (hardware-free).

These lock in the motor mappings taken from the official app so a refactor can't
silently break "forward is forward".
"""

import pytest

from apitor_ble.profiles import (
    PROFILES,
    RobotProfile,
    drive_directions,
    get_profile,
    motor_from_number,
    opposite,
)
from apitor_ble.protocol import Direction, Motor


def test_opposite():
    assert opposite(Direction.D1) is Direction.D2
    assert opposite(Direction.D2) is Direction.D1
    assert opposite(Direction.STOP) is Direction.STOP


def test_motor_from_number():
    assert motor_from_number(1) is Motor.M1
    assert motor_from_number(2) is Motor.M2
    assert motor_from_number(3) is Motor.M3
    with pytest.raises(ValueError):
        motor_from_number(0)


def test_get_profile_known_and_unknown():
    assert get_profile("j").product == "j"
    assert get_profile("J").product == "j"          # case-insensitive
    with pytest.raises(ValueError, match="Supported robots"):
        get_profile("z")


def test_all_products_present():
    assert set(PROFILES) == {"j", "s", "q", "r", "x", "w"}


def test_robot_j_matches_official_app_mapping():
    """Robot J: forward=M1:D2/M2:D1, back=M1:D1/M2:D2, right=both D1, left=both D2."""
    j = get_profile("j")
    # (left_motor, left_dir, right_motor, right_dir)
    fwd = drive_directions(j, True, True)
    back = drive_directions(j, False, False)
    left = drive_directions(j, False, True)
    right = drive_directions(j, True, False)

    def as_m1m2(result):
        lm, ld, rm, rd = result
        d = {lm: ld, rm: rd}
        return d[Motor.M1], d[Motor.M2]

    assert as_m1m2(fwd) == (Direction.D2, Direction.D1)
    assert as_m1m2(back) == (Direction.D1, Direction.D2)
    assert as_m1m2(right) == (Direction.D1, Direction.D1)
    assert as_m1m2(left) == (Direction.D2, Direction.D2)


def test_forward_and_backward_are_opposite_everywhere():
    for letter in PROFILES:
        p = get_profile(letter)
        _, fld, _, frd = drive_directions(p, True, True)
        _, bld, _, brd = drive_directions(p, False, False)
        assert bld is opposite(fld)
        assert brd is opposite(frd)


def test_flip_left_reverses_only_left_wheel():
    p = get_profile("j")
    flipped = p.with_overrides(flip_left=True)
    assert flipped.left_forward is opposite(p.left_forward)
    assert flipped.right_forward is p.right_forward
    assert flipped.calibrated is True  # any override counts as user-calibrated


def test_swap_motors_via_overrides():
    p = get_profile("j").with_overrides(left_motor=1, right_motor=2)
    assert p.left_motor is Motor.M1
    assert p.right_motor is Motor.M2


def test_profile_is_immutable():
    p = get_profile("j")
    with pytest.raises(Exception):
        p.left_motor = Motor.M3  # frozen dataclass
