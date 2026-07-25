"""apitor_ble - a small async library for driving Apitor BLE robots (e.g. Robot J).

Reverse-engineered from the official Apitor Kit Android app. See docs/ for the
protocol write-up. Public API:

    from apitor_ble import ApitorRobot, Motor, Direction, Color
    from apitor_ble.easy import Robot          # beginner-friendly wrapper
"""

from __future__ import annotations

from .easy import Robot as EasyRobot
from .exceptions import (
    ApitorError,
    AuthorizationError,
    ConnectionError,
    DiscoveryError,
    ProtocolError,
)
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

try:
    from .robot import ApitorRobot
except ImportError as _exc:  # bleak not installed -> protocol layer still usable
    _robot_import_error = _exc

    class ApitorRobot:  # type: ignore[no-redef]
        """Placeholder raised when the optional ``bleak`` dependency is missing."""

        def __init__(self, *args: object, **kwargs: object) -> None:
            raise ImportError(
                "apitor_ble.robot requires 'bleak'. Install it with: pip install bleak"
            ) from _robot_import_error


__version__ = "0.2.0"

__all__ = [
    # Core driver
    "ApitorRobot",
    "EasyRobot",
    # Enums / protocol
    "Motor",
    "Direction",
    "Color",
    "auth_frame",
    "motor_command",
    "led_command",
    "stop_all_command",
    "PRODUCT_KEYS",
    "UUID_SERVICE",
    "UUID_WRITE",
    "UUID_NOTIFY",
    "COMMAND_INTERVAL_S",
    # Notifications
    "SensorFrame",
    "FrameKind",
    "decode_notification",
    # Exceptions
    "ApitorError",
    "DiscoveryError",
    "ConnectionError",
    "AuthorizationError",
    "ProtocolError",
    "__version__",
]
