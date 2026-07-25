"""Command-line interface for apitor_ble.

Installed as the ``apitor`` console command::

    apitor scan                 # list nearby Apitor J robots
    apitor demo                 # connect, wiggle motors, blink LEDs
    apitor listen               # connect and print incoming notifications
    apitor drive                # keyboard-driven live control (type key + Enter)

Options:
    --product j        product letter (default: j)
    --address AA:BB..  skip scanning and connect straight to this address
    --timeout 10       scan timeout in seconds
    --verbose          enable debug logging (shows raw TX/RX frames)

This module owns all user-facing terminal output; the library itself only logs.
"""

from __future__ import annotations

import argparse
import asyncio
import logging
import sys
from collections.abc import Awaitable, Callable, Sequence

from . import __version__
from .exceptions import ApitorError
from .protocol import Color, Direction, Motor
from .robot import ApitorRobot
from .sensor import SensorFrame

log = logging.getLogger("apitor_ble.cli")


def _build_robot(args: argparse.Namespace) -> ApitorRobot | None:
    """Return a robot bound to ``--address``, or ``None`` to discover instead."""
    if args.address:
        return ApitorRobot(address=args.address, product=args.product)
    return None


async def _connect(args: argparse.Namespace) -> ApitorRobot:
    """Resolve and connect to a robot, honoring ``--address``/``--product``."""
    robot = _build_robot(args)
    if robot is None:
        robot = await ApitorRobot.discover(product=args.product, timeout=args.timeout)
    await robot.connect()
    return robot


async def cmd_scan(args: argparse.Namespace) -> int:
    """List nearby robots matching the selected product."""
    matches = await ApitorRobot.scan(product=args.product, timeout=args.timeout)
    if not matches:
        print(f"No Apitor '{args.product}' robots found.")
        return 1
    print(f"Found {len(matches)} device(s):")
    for device in matches:
        print(f"  {device.name:<20} {device.address}")
    return 0


async def cmd_demo(args: argparse.Namespace) -> int:
    """Connect and run a short motor + LED routine."""
    robot = await _connect(args)
    try:
        print("Connected. Running motor + LED demo...")
        print("  motor M1 forward (speed 8)")
        await robot.run_motor(Motor.M1, Direction.D1, speed=8)
        await asyncio.sleep(1.5)

        print("  motor M1 reverse (speed 8)")
        await robot.run_motor(Motor.M1, Direction.D2, speed=8)
        await asyncio.sleep(1.5)

        print("  stop all motors")
        await robot.stop_all_motors()

        for color in (Color.RED, Color.GREEN, Color.BLUE):
            print(f"  all LEDs {color.name}")
            await robot.all_leds(color)
            await asyncio.sleep(0.8)

        print("  LEDs off")
        await robot.all_leds(Color.OFF)
        print("Demo complete.")
        return 0
    finally:
        await robot.stop_all_motors()
        await robot.disconnect()


async def cmd_listen(args: argparse.Namespace) -> int:
    """Connect and print decoded notification frames until interrupted."""
    robot = _build_robot(args)
    if robot is None:
        robot = await ApitorRobot.discover(product=args.product, timeout=args.timeout)

    def on_frame(frame: SensorFrame) -> None:
        tag = "  [LOW BATTERY]" if frame.low_power else ""
        print(f"<- {frame.kind.name:<7} {frame.hex}{tag}")

    robot.on_sensor(on_frame)
    await robot.connect()
    print("Listening for decoded notifications. Press Ctrl+C to stop.")
    try:
        while robot.is_connected:
            await asyncio.sleep(0.5)
    except (KeyboardInterrupt, asyncio.CancelledError):
        pass
    finally:
        await robot.disconnect()
    return 0


async def cmd_drive(args: argparse.Namespace) -> int:
    """Small blocking-input driver: type a key + Enter to send a command."""
    robot = await _connect(args)
    print(
        "Live control. Commands (then Enter):\n"
        "  w/s = motor M1 fwd/rev   a/d = motor M2 fwd/rev\n"
        "  space = stop all         r/g/b = LED red/green/blue   o = LED off\n"
        "  q = quit"
    )
    loop = asyncio.get_event_loop()
    try:
        while True:
            key = (await loop.run_in_executor(None, sys.stdin.readline)).strip().lower()
            if key == "q":
                break
            elif key == "w":
                await robot.run_motor(Motor.M1, Direction.D1, 8)
            elif key == "s":
                await robot.run_motor(Motor.M1, Direction.D2, 8)
            elif key == "a":
                await robot.run_motor(Motor.M2, Direction.D1, 8)
            elif key == "d":
                await robot.run_motor(Motor.M2, Direction.D2, 8)
            elif key == "":
                continue
            elif key in ("space", " "):
                await robot.stop_all_motors()
            elif key == "r":
                await robot.all_leds(Color.RED)
            elif key == "g":
                await robot.all_leds(Color.GREEN)
            elif key == "b":
                await robot.all_leds(Color.BLUE)
            elif key == "o":
                await robot.all_leds(Color.OFF)
            else:
                await robot.stop_all_motors()
    finally:
        await robot.stop_all_motors()
        await robot.disconnect()
    return 0


COMMANDS: dict[str, Callable[[argparse.Namespace], Awaitable[int]]] = {
    "scan": cmd_scan,
    "demo": cmd_demo,
    "listen": cmd_listen,
    "drive": cmd_drive,
}


def build_parser() -> argparse.ArgumentParser:
    """Build the ``apitor`` argument parser."""
    parser = argparse.ArgumentParser(
        prog="apitor", description="Control Apitor BLE robots from the command line."
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("command", choices=COMMANDS.keys(), help="what to run")
    parser.add_argument("--product", default="j", help="product letter (default: j)")
    parser.add_argument("--address", default=None, help="connect directly to this BLE address")
    parser.add_argument("--timeout", type=float, default=10.0, help="scan timeout seconds")
    parser.add_argument("--verbose", action="store_true", help="debug logging")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Entry point for the ``apitor`` console script."""
    args = build_parser().parse_args(argv)
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s %(name)s: %(message)s",
    )
    try:
        return asyncio.run(COMMANDS[args.command](args))
    except ApitorError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        return 130


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
