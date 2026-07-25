"""Low-level protocol definitions for Apitor BLE robots.

Everything in this module is pure data / byte-building with no I/O, so it can be
unit-tested and reused independently of the BLE transport in ``robot.py``.

The raw numeric values live in :mod:`apitor_ble.constants`; this module gives
them protocol meaning (enums and frame builders). Reverse-engineered from the
official "Apitor Kit" Android app (``com.robot.apitor``, class
``com.robot.apitor.robot.Robot``). See ``docs/PROTOCOL.md`` for the full
write-up.
"""

from __future__ import annotations

from enum import IntEnum

from . import constants as c
from .exceptions import ProtocolError

# --------------------------------------------------------------------------- #
# GATT profile / transport (re-exported from constants for a stable public API)
# --------------------------------------------------------------------------- #
UUID_SERVICE = c.UUID_SERVICE
UUID_WRITE = c.UUID_WRITE
UUID_NOTIFY = c.UUID_NOTIFY
MAX_WRITE_CHUNK = c.MAX_WRITE_CHUNK
COMMAND_INTERVAL_S = c.COMMAND_INTERVAL_S
NAME_PREFIX = c.NAME_PREFIX


# --------------------------------------------------------------------------- #
# Per-product authorization handshake
# --------------------------------------------------------------------------- #
# Immediately after connecting, the robot ignores all commands until it receives
# this 20-byte "password" frame on the write characteristic. Frame layout is
# ``55 AA 11 20`` + 16 ASCII key bytes (Wheels uses ``55 AA 11 80``).
#
# Keyed by the product letter returned by ApitorPreference.getCurrentProdName().
PRODUCT_KEYS: dict[str, str] = {
    "j": "55aa1120436e354174675a4c4a7671723863447a",  # Robot J  -> "Cn5AtgZLJvqr8cDz"
    "s": "55aa11205572364f364d48524f6652416f4f5830",  # Robot S  -> "Ur6O6MHROfRAoOX0"
    "q": "55aa112064796f7a574f50663035326757565034",  # Robot Q  -> "dyozWOPf052gWVP4"
    "r": "55aa1120633942527a6161317850307136696b62",  # Robot R  -> "c9BRzaa1xP0q6ikb"
    "x": "55aa112055494d384c5679526e75706973654276",  # Robot X  -> "UIM8LVyRnupiseBv"
    "w": "55aa1180686c354174675b7d4a7276723863447a",  # Wheels   (non-ASCII payload)
}

# In the app any product without its own key falls back to Robot X's password.
DEFAULT_KEY = PRODUCT_KEYS["x"]


# --------------------------------------------------------------------------- #
# Command frame headers (2-byte framing + 1-byte command)
# --------------------------------------------------------------------------- #
HEADER_MOTOR = c.FRAME_HEADER + bytes((c.CMD_MOTOR,))
HEADER_LED = c.FRAME_HEADER + bytes((c.CMD_LED,))
HEADER_SENSOR = c.FRAME_HEADER + bytes((c.CMD_SENSOR, c.SENSOR_MODE))


class Motor(IntEnum):
    """Motor port index used in motor commands."""

    M1 = c.MOTOR_M1
    M2 = c.MOTOR_M2
    M3 = c.MOTOR_M3
    ALL = c.MOTOR_ALL
    STOP_ALL = c.MOTOR_STOP_ALL  # 0x10, only meaningful with direction=STOP, speed=0


class Direction(IntEnum):
    """Motor spin direction."""

    STOP = c.DIR_STOP
    D1 = c.DIR_D1  # one way
    D2 = c.DIR_D2  # the other way


class Color(IntEnum):
    """LED colors (values match the app's getColor mapping)."""

    OFF = c.COLOR_OFF
    RED = c.COLOR_RED
    ORANGE = c.COLOR_ORANGE
    YELLOW = c.COLOR_YELLOW
    GREEN = c.COLOR_GREEN
    CYAN = c.COLOR_CYAN
    BLUE = c.COLOR_BLUE
    PURPLE = c.COLOR_PURPLE
    WHITE = c.COLOR_WHITE


def _byte(value: int) -> int:
    """Clamp an int into a single unsigned byte, mirroring the app's (byte) casts."""
    return value & 0xFF


def auth_frame(product: str) -> bytes:
    """Return the authorization ("password") frame for a product letter.

    ``product`` is a single letter such as ``"j"``. Unknown products fall back to
    the Robot X key, exactly as the app does.
    """
    key_hex = PRODUCT_KEYS.get(product.lower().strip(), DEFAULT_KEY)
    return bytes.fromhex(key_hex)


def motor_command(motor: int, direction: int, speed: int) -> bytes:
    """Build a motor command: ``55 AA 03 <motor> <direction> <speed>``.

    ``speed`` is 0-12 in the app's UI (S1-S12); higher values are accepted by
    the frame but not exposed by the app. Values are masked into a single byte,
    matching the app's ``(byte)`` casts.
    """
    return HEADER_MOTOR + bytes((_byte(motor), _byte(direction), _byte(speed)))


def stop_all_command() -> bytes:
    """Build the "stop every motor" command: ``55 AA 03 10 00 00``."""
    return motor_command(Motor.STOP_ALL, Direction.STOP, 0)


def led_command(index: int, color: int) -> bytes:
    """Build an LED command: ``55 AA 04 <index> <color> 00 00``.

    ``index`` selects which LED (1, 2, ...); the app uses index 4 as an
    "all LEDs" shortcut. Two trailing zero bytes are always appended.
    """
    return HEADER_LED + bytes((_byte(index), _byte(color), 0x00, 0x00))


def device_name_matches(name: str | None, product: str) -> bool:
    """Return ``True`` if an advertised ``name`` belongs to the given product.

    Mirrors ``Robot.isApitorDevice``: name starts with ``"apitort" + product``,
    compared case-insensitively after trimming.
    """
    if not name:
        return False
    expected = (NAME_PREFIX + product).lower()
    return name.strip().lower().startswith(expected)


def chunk_write(data: bytes, size: int = MAX_WRITE_CHUNK) -> list[bytes]:
    """Split ``data`` into ``<=size`` byte chunks, matching setSplitWriteNum(20).

    Raises :class:`~apitor_ble.exceptions.ProtocolError` if ``size`` is not
    positive.
    """
    if size <= 0:
        raise ProtocolError(f"chunk size must be positive, got {size}")
    return [data[i : i + size] for i in range(0, len(data), size)] or [b""]
