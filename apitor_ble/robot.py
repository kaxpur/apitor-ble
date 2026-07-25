"""Async BLE driver for Apitor robots, built on `bleak`.

Example
-------
    import asyncio
    from apitor_ble import ApitorRobot, Motor, Direction

    async def main():
        robot = await ApitorRobot.discover(product="j")
        async with robot:
            await robot.run_motor(Motor.M1, Direction.D1, speed=8)
            await asyncio.sleep(2)
            await robot.stop_all_motors()

    asyncio.run(main())
"""

from __future__ import annotations

import asyncio
import logging
from collections.abc import Callable

from bleak import BleakClient, BleakScanner
from bleak.backends.device import BLEDevice

from . import protocol as p
from .exceptions import (
    ApitorError,
    AuthorizationError,
    ConnectionError,
    DiscoveryError,
)
from .protocol import Color, Direction, Motor
from .sensor import SensorFrame, decode_notification

log = logging.getLogger("apitor_ble")

NotifyCallback = Callable[[bytes], None]
SensorCallback = Callable[[SensorFrame], None]

__all__ = [
    "ApitorRobot",
    "ApitorError",
    "AuthorizationError",
    "ConnectionError",
    "DiscoveryError",
]


class ApitorRobot:
    """A single Apitor robot over BLE.

    Parameters
    ----------
    address:
        The BLE MAC / UUID address to connect to. Optional if you use
        :meth:`discover`, which fills it in for you.
    product:
        Single product letter (``"j"`` for Robot J). Selects the authorization
        key and the advertised-name filter. Defaults to ``"j"``.
    device:
        An already-resolved ``BLEDevice`` (as returned by bleak's scanner). If
        given, it takes priority over ``address``.
    """

    def __init__(
        self,
        address: str | None = None,
        product: str = "j",
        device: BLEDevice | None = None,
    ) -> None:
        if device is None and address is None:
            raise ValueError("Provide either an address, a device, or use discover().")
        self.product = product.lower().strip()
        self._device = device
        self._address = device.address if device is not None else address
        self._client: BleakClient | None = None
        self._notify_cb: NotifyCallback | None = None
        self._sensor_cb: SensorCallback | None = None
        self._last_low_power: bool | None = None
        # Serializes writes so we never overlap GATT operations.
        self._write_lock = asyncio.Lock()

    # ------------------------------------------------------------------ #
    # Discovery
    # ------------------------------------------------------------------ #
    @classmethod
    async def scan(cls, product: str = "j", timeout: float = 10.0) -> list[BLEDevice]:
        """Scan and return all advertising devices matching ``product``.

        Filtering is done by advertised name (``apitort<product>``), the same
        way the official app does.
        """
        product = product.lower().strip()
        log.info("Scanning %.1fs for Apitor '%s' devices...", timeout, product)
        found = await BleakScanner.discover(timeout=timeout, service_uuids=[p.UUID_SERVICE])
        matches = [d for d in found if p.device_name_matches(d.name, product)]
        log.info(
            "Found %d matching device(s): %s",
            len(matches),
            [f"{d.name} ({d.address})" for d in matches],
        )
        return matches

    @classmethod
    async def discover(cls, product: str = "j", timeout: float = 10.0) -> ApitorRobot:
        """Scan and return an :class:`ApitorRobot` bound to the first match.

        Raises :class:`ApitorError` if nothing matching is found.
        """
        matches = await cls.scan(product=product, timeout=timeout)
        if not matches:
            raise DiscoveryError(
                f"No Apitor '{product}' robot found. Is it powered on and in range?"
            )
        return cls(device=matches[0], product=product)

    # ------------------------------------------------------------------ #
    # Connection lifecycle
    # ------------------------------------------------------------------ #
    @property
    def is_connected(self) -> bool:
        return self._client is not None and self._client.is_connected

    def on_notify(self, callback: NotifyCallback | None) -> None:
        """Register a callback for raw notification frames from the robot."""
        self._notify_cb = callback

    def on_sensor(self, callback: SensorCallback | None) -> None:
        """Register a callback for decoded :class:`SensorFrame` notifications."""
        self._sensor_cb = callback

    @property
    def low_power(self) -> bool | None:
        """Last known low-battery state, or None if no sensor frame seen yet."""
        return self._last_low_power

    async def connect(self) -> None:
        """Connect, subscribe to notifications, and send the auth handshake.

        Raises
        ------
        ConnectionError
            If the BLE link cannot be established.
        AuthorizationError
            If the authorization handshake could not be sent.
        """
        if self.is_connected:
            return
        target = self._device if self._device is not None else self._address
        log.info("Connecting to %s ...", self._address)
        self._client = BleakClient(target)
        try:
            await self._client.connect()
        except Exception as exc:  # noqa: BLE001 - normalize any bleak error
            self._client = None
            raise ConnectionError(f"Failed to connect to {self._address}: {exc}") from exc
        if not self._client.is_connected:
            self._client = None
            raise ConnectionError(f"Failed to connect to {self._address}")

        await self._client.start_notify(p.UUID_NOTIFY, self._handle_notify)
        # Authorize BEFORE any command, or the robot silently ignores everything.
        try:
            await self.authorize()
        except Exception as exc:  # noqa: BLE001 - normalize any bleak error
            raise AuthorizationError(
                f"Authorization handshake failed for product '{self.product}': {exc}"
            ) from exc
        log.info("Connected and authorized (%s).", self.product)

    async def disconnect(self) -> None:
        """Stop notifications and drop the BLE link."""
        if self._client is None:
            return
        try:
            if self._client.is_connected:
                try:
                    await self._client.stop_notify(p.UUID_NOTIFY)
                except Exception:  # noqa: BLE001 - best-effort cleanup
                    pass
                await self._client.disconnect()
        finally:
            self._client = None

    async def __aenter__(self) -> ApitorRobot:
        await self.connect()
        return self

    async def __aexit__(self, *exc) -> None:
        await self.disconnect()

    # ------------------------------------------------------------------ #
    # Low-level write
    # ------------------------------------------------------------------ #
    async def send_raw(self, data: bytes, *, response: bool = False) -> None:
        """Write raw bytes to the robot, split into 20-byte GATT chunks.

        This is the single choke-point every higher-level command goes through.
        """
        if not self.is_connected:
            raise ConnectionError("Not connected.")
        async with self._write_lock:
            for chunk in p.chunk_write(data):
                await self._client.write_gatt_char(p.UUID_WRITE, chunk, response=response)
            log.debug("-> %s", data.hex())

    async def authorize(self) -> None:
        """Send the per-product authorization frame."""
        await self.send_raw(p.auth_frame(self.product))

    def _handle_notify(self, _sender, data: bytearray) -> None:
        frame = bytes(data)
        log.debug("<- %s", frame.hex())
        if self._notify_cb is not None:
            self._notify_cb(frame)
        if self._sensor_cb is not None:
            decoded = decode_notification(frame)
            self._last_low_power = decoded.low_power
            self._sensor_cb(decoded)

    # ------------------------------------------------------------------ #
    # High-level robot API
    # ------------------------------------------------------------------ #
    async def run_motor(self, motor: Motor | int, direction: Direction | int, speed: int) -> None:
        """Drive one motor. ``speed`` is 0-12 (matches the app's S1-S12)."""
        await self.send_raw(p.motor_command(int(motor), int(direction), int(speed)))

    async def stop_motor(self, motor: Motor | int) -> None:
        """Stop a single motor."""
        await self.run_motor(motor, Direction.STOP, 0)

    async def stop_all_motors(self) -> None:
        """Stop every motor at once."""
        await self.send_raw(p.stop_all_command())

    async def set_led(self, index: int, color: Color | int) -> None:
        """Set an LED to a color. ``index`` selects the LED; 4 = all LEDs."""
        await self.send_raw(p.led_command(int(index), int(color)))

    async def all_leds(self, color: Color | int) -> None:
        """Set all LEDs to a color (uses LED index 4)."""
        await self.set_led(4, color)
