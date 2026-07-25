"""Tests for the pure (hardware-free) helpers in apitor_ble.easy.

These cover the name/number translations a beginner relies on, without needing a
robot or bleak.
"""

import pytest

from apitor_ble.easy import (
    _clamp_speed,
    _color_value,
    _direction_value,
    _motor_value,
)
from apitor_ble.protocol import Color, Direction, Motor


def test_color_names_map_to_values():
    assert _color_value("blue") is Color.BLUE
    assert _color_value("OFF") is Color.OFF
    assert _color_value("  Purple ") is Color.PURPLE


def test_unknown_color_is_a_friendly_error():
    with pytest.raises(ValueError, match="I don't know the color"):
        _color_value("sparkles")


def test_motor_numbers_map_to_ports():
    assert _motor_value(1) is Motor.M1
    assert _motor_value(2) is Motor.M2
    assert _motor_value(3) is Motor.M3


def test_bad_motor_number_is_rejected():
    with pytest.raises(ValueError, match="1, 2, or 3"):
        _motor_value(4)


@pytest.mark.parametrize("word", ["forward", "Forward", "f", "1"])
def test_forward_directions(word):
    assert _direction_value(word) is Direction.D1


@pytest.mark.parametrize("word", ["backward", "back", "reverse", "b", "2"])
def test_backward_directions(word):
    assert _direction_value(word) is Direction.D2


def test_bad_direction_is_rejected():
    with pytest.raises(ValueError, match="forward"):
        _direction_value("sideways")


def test_speed_is_clamped_between_1_and_10():
    assert _clamp_speed(5) == 5
    assert _clamp_speed(0) == 1
    assert _clamp_speed(-3) == 1
    assert _clamp_speed(99) == 10
    assert _clamp_speed(7.4) == 7
