"""apitor_ble - a small async library for driving Apitor BLE robots (e.g. Robot J).

Reverse-engineered from the official Apitor Kit Android app. See docs/ for the
protocol write-up. Public API:

    from apitor_ble import ApitorRobot, Motor, Direction, Color
"""

from .protocol import (
    COMMAND_INTERVAL_S,
    PRODUCT_KEYS,
    UUID_NOTIFY,
    UUID_SERVICE,
    UUID_WRITE,
    Color,
    Direction,
    Motor,
    auth_frame,
    led_command,
    motor_command,
    stop_all_command,
)
from .sensor import FrameKind, SensorFrame, decode_notification
from .easy import Robot as EasyRobot
try:
    from .robot import ApitorError, ApitorRobot
except ImportError as _exc:  # bleak not installed -> protocol layer still usable
    _robot_import_error = _exc

    class _MissingBleak:
        def __init__(self, *a, **k):
            raise ImportError(
                "apitor_ble.robot requires 'bleak'. Install it with: pip install bleak"
            ) from _robot_import_error

    class ApitorRobot(_MissingBleak):  # type: ignore[no-redef]
        pass

    class ApitorError(RuntimeError):  # type: ignore[no-redef]
        pass

__version__ = "0.1.0"

__all__ = [
    "ApitorRobot",
    "ApitorError",
    "EasyRobot",
    "Motor",
    "Direction",
    "Color",
    "SensorFrame",
    "FrameKind",
    "decode_notification",
    "auth_frame",
    "motor_command",
    "led_command",
    "stop_all_command",
    "PRODUCT_KEYS",
    "UUID_SERVICE",
    "UUID_WRITE",
    "UUID_NOTIFY",
    "COMMAND_INTERVAL_S",
    "__version__",
]
