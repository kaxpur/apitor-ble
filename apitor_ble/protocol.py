"""Low-level protocol definitions for Apitor BLE robots.

Everything in this module is pure data / byte-building with no I/O, so it can be
unit-tested and reused independently of the BLE transport in ``robot.py``.

Reverse-engineered from the official "Apitor Kit" Android app
(``com.robot.apitor``, class ``com.robot.apitor.robot.Robot``). See
``docs/PROTOCOL.md`` for the full write-up.
"""

from __future__ import annotations

from enum import IntEnum

# --------------------------------------------------------------------------- #
# GATT profile (identical across all Apitor products)
# --------------------------------------------------------------------------- #
# Nordic-style UART service. The 16-bit shortcuts are 0xF0FF / 0xF001 / 0xF002.
UUID_SERVICE = "0000f0ff-0000-1000-8000-00805f9b34fb"
UUID_WRITE = "0000f001-0000-1000-8000-00805f9b34fb"  # phone -> robot
UUID_NOTIFY = "0000f002-0000-1000-8000-00805f9b34fb"  # robot -> phone

# The app splits every GATT write into <=20 byte chunks (setSplitWriteNum(20)).
MAX_WRITE_CHUNK = 20

# The app throttles outgoing commands to one per ~500 ms (CMD_INTERVAL_MS).
COMMAND_INTERVAL_S = 0.5

# Advertised name prefix: "apitort" + product letter, matched case-insensitively.
NAME_PREFIX = "apitort"


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
# Command frame headers
# --------------------------------------------------------------------------- #
HEADER_MOTOR = bytes.fromhex("55AA03")
HEADER_LED = bytes.fromhex("55AA04")
HEADER_SENSOR = bytes.fromhex("55AA0580")


class Motor(IntEnum):
    """Motor port index used in motor commands."""

    M1 = 6
    M2 = 7
    M3 = 8
    ALL = 9
    STOP_ALL = 16  # 0x10, only meaningful with direction=STOP, speed=0


class Direction(IntEnum):
    STOP = 0
    D1 = 1  # one way
    D2 = 2  # the other way


class Color(IntEnum):
    """LED colors (values match the app's getColor mapping)."""

    OFF = 0
    RED = 1
    ORANGE = 2
    YELLOW = 3
    GREEN = 4
    CYAN = 5
    BLUE = 6
    PURPLE = 7
    WHITE = 10


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
    the frame but not exposed by the app.
    """
    return HEADER_MOTOR + bytes([_byte(motor), _byte(direction), _byte(speed)])


def stop_all_command() -> bytes:
    """Build the "stop every motor" command: ``55 AA 03 10 00 00``."""
    return motor_command(Motor.STOP_ALL, Direction.STOP, 0)


def led_command(index: int, color: int) -> bytes:
    """Build an LED command: ``55 AA 04 <index> <color> 00 00``.

    ``index`` selects which LED (1, 2, ...); the app uses index 4 as an
    "all LEDs" shortcut. Two trailing zero bytes are always appended.
    """
    return HEADER_LED + bytes([_byte(index), _byte(color), 0x00, 0x00])


def device_name_matches(name: str | None, product: str) -> bool:
    """Return True if an advertised ``name`` belongs to the given product.

    Mirrors ``Robot.isApitorDevice``: name starts with ``"apitort" + product``,
    compared case-insensitively after trimming.
    """
    if not name:
        return False
    expected = (NAME_PREFIX + product).lower()
    return name.strip().lower().startswith(expected)


def chunk_write(data: bytes, size: int = MAX_WRITE_CHUNK) -> list[bytes]:
    """Split ``data`` into <=``size`` byte chunks, matching setSplitWriteNum(20)."""
    return [data[i : i + size] for i in range(0, len(data), size)] or [b""]
