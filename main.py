#!/usr/bin/env python3
"""Interactive test / demo script for the apitor_ble library.

Usage:
    python main.py scan                 # list nearby Apitor J robots
    python main.py demo                 # connect, wiggle motors, blink LEDs
    python main.py listen               # connect and print incoming notifications
    python main.py drive                # keyboard-driven live control (WASD)

Options:
    --product j        product letter (default: j)
    --address AA:BB..  skip scanning and connect straight to this address
    --timeout 10       scan timeout in seconds
    --verbose          enable debug logging (shows raw TX/RX frames)
"""

from __future__ import annotations

import argparse
import asyncio
import logging
import sys

from apitor_ble import ApitorRobot, Color, Direction, Motor, SensorFrame
from apitor_ble.robot import ApitorError


def _build_robot(args) -> ApitorRobot | None:
    """Return a robot bound to --address, or None if we should discover instead."""
    if args.address:
        return ApitorRobot(address=args.address, product=args.product)
    return None


async def cmd_scan(args) -> int:
    matches = await ApitorRobot.scan(product=args.product, timeout=args.timeout)
    if not matches:
        print(f"No Apitor '{args.product}' robots found.")
        return 1
    print(f"Found {len(matches)} device(s):")
    for d in matches:
        print(f"  {d.name:<20} {d.address}")
    return 0


async def _connect(args) -> ApitorRobot:
    robot = _build_robot(args)
    if robot is None:
        robot = await ApitorRobot.discover(product=args.product, timeout=args.timeout)
    await robot.connect()
    return robot


async def cmd_demo(args) -> int:
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


async def cmd_listen(args) -> int:
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


async def cmd_drive(args) -> int:
    """Very small blocking-input driver: type a key + Enter."""
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
            elif key == "space" or key == " ":
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


COMMANDS = {
    "scan": cmd_scan,
    "demo": cmd_demo,
    "listen": cmd_listen,
    "drive": cmd_drive,
}


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="apitor_ble test harness")
    parser.add_argument("command", choices=COMMANDS.keys(), help="what to run")
    parser.add_argument("--product", default="j", help="product letter (default: j)")
    parser.add_argument("--address", default=None, help="connect directly to this BLE address")
    parser.add_argument("--timeout", type=float, default=10.0, help="scan timeout seconds")
    parser.add_argument("--verbose", action="store_true", help="debug logging")
    return parser.parse_args(argv)


def main(argv=None) -> int:
    args = parse_args(argv)
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s %(name)s: %(message)s",
    )
    try:
        return asyncio.run(COMMANDS[args.command](args))
    except ApitorError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
