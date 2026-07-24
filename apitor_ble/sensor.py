"""Decoding of notification frames sent by the robot (robot -> phone, on 0xF002).

The app (`Robot.onMessage`) recognizes two notification shapes:

* **Sensor frames** (header ``55 AA 05 80``). Byte index 7 == 2 signals low
  battery; the rest of the payload is relayed to the app's Scratch/JS layer and
  its per-attachment meaning is not otherwise decoded by the app.
* **Wheels sensor frames** (only the "Wheels" product). These carry motion
  feedback: remaining move distance, order-buffer size, and an
  "action finished" flag. Robot J does **not** use these.

This module exposes what the app actually acts on, and keeps the raw bytes so
callers can do their own decoding. See ``docs/PROTOCOL.md`` section 5.3.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum
from typing import Optional

# Header that marks a standard sensor/telemetry frame (matches HEADER_SENSOR).
SENSOR_PREFIX = "55aa0580"


class FrameKind(IntEnum):
    UNKNOWN = 0
    SENSOR = 2  # 55 AA 05 80 ...  (Robot J and other standard products)
    WHEELS = 3  # Wheels-only motion feedback


@dataclass
class SensorFrame:
    """A decoded notification frame.

    Attributes
    ----------
    raw:
        The exact bytes received.
    kind:
        Which shape we recognized (:class:`FrameKind`).
    low_power:
        True if the robot is reporting a low battery.
    wheel_distance / order_buffer_size / order_action_end:
        Wheels-only motion feedback; ``None`` for Robot J and other products.
    """

    raw: bytes
    kind: FrameKind = FrameKind.UNKNOWN
    low_power: bool = False
    wheel_distance: Optional[int] = None
    order_buffer_size: Optional[int] = None
    order_action_end: Optional[bool] = None

    @property
    def hex(self) -> str:
        return self.raw.hex()

    @property
    def is_sensor(self) -> bool:
        return self.kind is FrameKind.SENSOR

    @property
    def payload(self) -> bytes:
        """Bytes after the 4-byte ``55 AA 05 80`` header (sensor frames)."""
        return self.raw[4:] if self.is_sensor else b""

    def __repr__(self) -> str:  # concise, useful when printing live frames
        bits = [f"kind={self.kind.name}", f"hex={self.hex}"]
        if self.low_power:
            bits.append("LOW_POWER")
        if self.kind is FrameKind.WHEELS:
            bits.append(
                f"dist={self.wheel_distance} buf={self.order_buffer_size} "
                f"end={self.order_action_end}"
            )
        return f"SensorFrame({', '.join(bits)})"


def _b(frame: bytes, i: int) -> int:
    """Byte at index ``i`` or 0 if out of range (mirrors Command.get)."""
    return frame[i] if 0 <= i < len(frame) else 0


def decode_notification(raw: bytes) -> SensorFrame:
    """Decode a raw notification frame into a :class:`SensorFrame`.

    Never raises on short/unknown input: unrecognized frames come back with
    ``kind=UNKNOWN`` and their raw bytes preserved.
    """
    data = bytes(raw)
    hex_str = data.hex().lower()

    if hex_str.startswith(SENSOR_PREFIX):
        # Standard sensor frame. The app treats byte[7]==2 as low battery.
        return SensorFrame(
            raw=data,
            kind=FrameKind.SENSOR,
            low_power=_b(data, 7) == 2,
        )

    if _is_wheels_frame(data):
        # Wheels motion feedback (see Robot.onMessage, type == 3 branch).
        distance = _b(data, 4)
        if distance == 4:  # app remaps a "4" distance to 0
            distance = 0
        return SensorFrame(
            raw=data,
            kind=FrameKind.WHEELS,
            low_power=_b(data, 5) == 2,
            wheel_distance=distance,
            order_buffer_size=_b(data, 6),
            order_action_end=_b(data, 8) == 0,
        )

    return SensorFrame(raw=data, kind=FrameKind.UNKNOWN)


def _is_wheels_frame(data: bytes) -> bool:
    """Heuristic for Wheels motion-feedback frames.

    The app's builder classifies these as a distinct type; here we recognize the
    ``55 AA ..`` framing that is not the standard sensor header. This is only
    relevant for the Wheels product, never Robot J.
    """
    return len(data) >= 9 and data[0] == 0x55 and data[1] == 0xAA and not data.hex().lower().startswith(SENSOR_PREFIX) and data[2] in (0x03, 0x02)
