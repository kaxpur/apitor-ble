"""Low-level wire constants for the Apitor BLE protocol.

Everything here is a plain, named value — no logic — so the rest of the library
can refer to meaningful names instead of magic numbers like ``0x55`` or ``0x03``.

Grouped by role:

* **Framing** — the two bytes every frame starts with.
* **Command bytes** — the frame "type" that follows the header.
* **Motor / LED / auth fields** — the parameter values used inside frames.
* **GATT** — service/characteristic UUIDs and transport limits.

See ``docs/PROTOCOL.md`` for the byte-level write-up these values come from.
"""

from __future__ import annotations

from typing import Final

# --------------------------------------------------------------------------- #
# Frame framing
# --------------------------------------------------------------------------- #
# Every frame (both directions) begins with these two bytes.
FRAME_HEADER_0: Final = 0x55
FRAME_HEADER_1: Final = 0xAA
FRAME_HEADER: Final = bytes((FRAME_HEADER_0, FRAME_HEADER_1))

# --------------------------------------------------------------------------- #
# Command bytes (the frame "type", following the 2-byte header)
# --------------------------------------------------------------------------- #
CMD_MOTOR: Final = 0x03  # drive a motor
CMD_LED: Final = 0x04  # set an LED color
CMD_SENSOR: Final = 0x05  # sensor / telemetry (used in notifications)
CMD_AUTH: Final = 0x11  # authorization ("password") frame

# --------------------------------------------------------------------------- #
# Authorization frame
# --------------------------------------------------------------------------- #
# The auth command byte is followed by a length/mode byte, then the key bytes.
AUTH_MODE_STANDARD: Final = 0x20  # most products: header 55 AA 11 20
AUTH_MODE_WHEELS: Final = 0x80  # the "Wheels" product: header 55 AA 11 80

# --------------------------------------------------------------------------- #
# Motor command fields
# --------------------------------------------------------------------------- #
# Motor "port" selector.
MOTOR_M1: Final = 0x06
MOTOR_M2: Final = 0x07
MOTOR_M3: Final = 0x08
MOTOR_ALL: Final = 0x09
MOTOR_STOP_ALL: Final = 0x10  # only meaningful with direction=STOP, speed=0

# Motor direction.
DIR_STOP: Final = 0x00
DIR_D1: Final = 0x01  # one way
DIR_D2: Final = 0x02  # the other way

# Speed range accepted by the frame (the app's UI exposes S1-S12).
SPEED_MIN: Final = 0
SPEED_MAX: Final = 12

# --------------------------------------------------------------------------- #
# LED command fields
# --------------------------------------------------------------------------- #
LED_ALL_INDEX: Final = 0x04  # the app's "all LEDs" shortcut index

# Color values (match the app's getColor mapping).
COLOR_OFF: Final = 0
COLOR_RED: Final = 1
COLOR_ORANGE: Final = 2
COLOR_YELLOW: Final = 3
COLOR_GREEN: Final = 4
COLOR_CYAN: Final = 5
COLOR_BLUE: Final = 6
COLOR_PURPLE: Final = 7
COLOR_WHITE: Final = 10

# --------------------------------------------------------------------------- #
# Sensor / notification fields
# --------------------------------------------------------------------------- #
# In a standard sensor frame (55 AA 05 80 ...), byte[7] == 2 signals low battery.
SENSOR_MODE: Final = 0x80
SENSOR_LOW_BATTERY_INDEX: Final = 7
SENSOR_LOW_BATTERY_VALUE: Final = 2

# --------------------------------------------------------------------------- #
# GATT profile (identical across all Apitor products)
# --------------------------------------------------------------------------- #
# Nordic-style UART service. The 16-bit shortcuts are 0xF0FF / 0xF001 / 0xF002.
UUID_SERVICE: Final = "0000f0ff-0000-1000-8000-00805f9b34fb"
UUID_WRITE: Final = "0000f001-0000-1000-8000-00805f9b34fb"  # phone -> robot
UUID_NOTIFY: Final = "0000f002-0000-1000-8000-00805f9b34fb"  # robot -> phone

# The app splits every GATT write into <=20 byte chunks (setSplitWriteNum(20)).
MAX_WRITE_CHUNK: Final = 20

# The app throttles outgoing commands to one per ~500 ms (CMD_INTERVAL_MS).
COMMAND_INTERVAL_S: Final = 0.5

# Advertised name prefix: "apitort" + product letter, matched case-insensitively.
NAME_PREFIX: Final = "apitort"
