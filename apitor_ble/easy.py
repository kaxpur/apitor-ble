"""A super-simple way to control Apitor robots — made for beginners.

This is a friendly wrapper around the full :class:`apitor_ble.ApitorRobot` API.
It hides the tricky parts (Bluetooth, ``async``/``await``, byte frames) so you
can write short, readable programs like this:

    from apitor_ble.easy import Robot

    robot = Robot()          # Robot J by default
    robot.connect()

    robot.forward(2)        # drive forward for 2 seconds
    robot.turn_left(1)      # turn left for 1 second
    robot.color("blue")     # make the lights blue
    robot.wait(1)           # wait 1 second
    robot.lights_off()

    robot.disconnect()

Everything here is *blocking* and reads top-to-bottom, so there is no ``async``,
no event loop to think about, and no callbacks.

Using a different robot
-----------------------
Pass ``product`` for another Apitor kit (``"s"``, ``"q"``, ``"r"``, ``"x"``,
``"w"``)::

    robot = Robot(product="s")

Every Apitor robot drives with **motor 1 and motor 2**, but which motor is the
left/right wheel — and which way is "forward" — depends on how the kit was
built. Robot J's default is verified on real hardware; the others use the
official app's standard-build values. If forward/turns come out wrong, calibrate
them (no code editing needed)::

    robot = Robot(product="s", flip_left=True)          # left wheel was reversed
    robot = Robot(product="s", left_motor=2, right_motor=1)  # wheels swapped

See ``docs/EASY.md`` for the full step-by-step, and ``docs/ROBOTS.md`` for the
official per-model motor tables.
"""

from __future__ import annotations

import asyncio
import threading
from collections.abc import Awaitable
from typing import TypeVar

from . import profiles
from .profiles import RobotProfile, drive_directions, motor_from_number
from .protocol import Color, Direction, Motor

_T = TypeVar("_T")

# ---- pure helpers (no robot needed — easy to test) ------------------------- #

# Friendly color names a student might type -> the real Color value.
_COLORS = {
    "off": Color.OFF,
    "red": Color.RED,
    "orange": Color.ORANGE,
    "yellow": Color.YELLOW,
    "green": Color.GREEN,
    "cyan": Color.CYAN,
    "blue": Color.BLUE,
    "purple": Color.PURPLE,
    "white": Color.WHITE,
}


def _color_value(color: str) -> Color:
    """Turn a color name like ``"blue"`` into the value the robot understands."""
    key = str(color).strip().lower()
    if key not in _COLORS:
        names = ", ".join(_COLORS)
        raise ValueError(f"I don't know the color '{color}'. Try one of: {names}.")
    return _COLORS[key]


def _motor_value(number: int) -> Motor:
    """Turn a motor number (1, 2, or 3) into the real motor port."""
    return motor_from_number(number)


def _direction_value(direction: str) -> Direction:
    """Turn ``"forward"``/``"backward"`` into the robot's direction value."""
    key = str(direction).strip().lower()
    if key in ("forward", "f", "1"):
        return Direction.D1
    if key in ("backward", "back", "reverse", "b", "2"):
        return Direction.D2
    raise ValueError("Direction must be 'forward' or 'backward'.")


def _clamp_speed(speed: int) -> int:
    """Keep speed sensible: 1 (slow) to 10 (fast)."""
    try:
        speed = int(round(speed))
    except (TypeError, ValueError):
        raise ValueError("Speed must be a number from 1 to 10.") from None
    return max(1, min(10, speed))


# ---- the friendly robot ---------------------------------------------------- #


class Robot:
    """An easy-to-use Apitor robot.

    Make one, call :meth:`connect`, then tell it what to do. Call
    :meth:`disconnect` (or use ``with Robot() as robot:``) when you are done.

    Parameters
    ----------
    product:
        Which Apitor kit: ``"j"`` (default), ``"s"``, ``"q"``, ``"r"``, ``"x"``,
        or ``"w"`` (Wheels).
    address:
        Usually leave this out and the robot is found for you. If you know your
        robot's Bluetooth address you can pass it, e.g.
        ``Robot(address="EB:28:75:C0:66:07")``.
    left_motor / right_motor:
        Calibration: which motor number (1-3) is the left / right wheel.
    flip_left / flip_right:
        Calibration: reverse a wheel whose "forward" goes the wrong way.
    profile:
        Advanced: a fully specified :class:`~apitor_ble.profiles.RobotProfile`
        (overrides ``product`` and the calibration options above).
    quiet:
        Pass ``quiet=True`` to stop the friendly print messages.
    """

    def __init__(
        self,
        product: str = "j",
        address: str | None = None,
        *,
        left_motor: int | None = None,
        right_motor: int | None = None,
        flip_left: bool = False,
        flip_right: bool = False,
        profile: RobotProfile | None = None,
        quiet: bool = False,
    ) -> None:
        base = profile if profile is not None else profiles.get_profile(product)
        self._profile = base.with_overrides(
            left_motor=left_motor,
            right_motor=right_motor,
            flip_left=flip_left,
            flip_right=flip_right,
        )
        self._address = address
        self._quiet = quiet
        self._robot = None  # the real ApitorRobot, created on connect()
        # A little background helper runs the Bluetooth work for us so you never
        # have to deal with async/await.
        self._loop = asyncio.new_event_loop()
        self._thread = threading.Thread(target=self._loop.run_forever, daemon=True)
        self._thread.start()

    # -- internal plumbing --------------------------------------------------- #
    def _say(self, message: str) -> None:
        """Print a friendly status message to the beginner.

        This is the *only* place the library writes to stdout, and it is a
        deliberate feature of the ``easy`` layer (not debug output). Silence it
        with ``Robot(quiet=True)``. Everything else in the library uses
        :mod:`logging`.
        """
        if self._quiet:
            return
        # Some terminals (e.g. the default Windows console) can't print every
        # character. Never let a friendly message crash a beginner's program.
        try:
            print(message)
        except UnicodeEncodeError:
            print(message.encode("ascii", "replace").decode("ascii"))

    def _run(self, coro: Awaitable[_T]) -> _T:
        """Run one async job on the background helper and wait for it to finish."""
        return asyncio.run_coroutine_threadsafe(coro, self._loop).result()

    def _require_connection(self) -> None:
        if self._robot is None:
            raise RuntimeError("The robot isn't connected yet. Call robot.connect() first.")

    # -- connecting ---------------------------------------------------------- #
    def connect(self, timeout: float = 10.0) -> Robot:
        """Find the robot and connect to it. Do this before anything else."""
        # Imported here so the pure helpers above work even without bleak.
        from .robot import ApitorError, ApitorRobot

        if self._robot is not None:
            return self  # already connected

        self._say(f"Looking for your {self._profile.name}... (make sure it's turned on!)")

        async def _do_connect():
            if self._address:
                robot = ApitorRobot(address=self._address, product=self._profile.product)
            else:
                robot = await ApitorRobot.discover(product=self._profile.product, timeout=timeout)
            await robot.connect()
            return robot

        try:
            self._robot = self._run(_do_connect())
        except ApitorError as exc:
            raise RuntimeError("I couldn't find your robot. Is it turned on and nearby?") from exc
        self._say("Connected! Your robot is ready.")
        if not self._profile.calibrated:
            self._say(
                f"  (Heads up: driving directions for {self._profile.name} haven't been\n"
                "   checked on a real robot yet. If forward or turning goes the wrong\n"
                "   way, see 'Setting up a different robot' in docs/EASY.md.)"
            )
        return self

    def disconnect(self) -> None:
        """Stop the robot and hang up the Bluetooth connection."""
        if self._robot is not None:
            self._run(self._robot.stop_all_motors())
            self._run(self._robot.disconnect())
            self._robot = None
            self._say("Goodbye! Robot disconnected.")
        # Stop the background helper.
        self._loop.call_soon_threadsafe(self._loop.stop)

    # Let people write:  with Robot() as robot: ...
    def __enter__(self) -> Robot:
        return self.connect()

    def __exit__(self, *exc) -> None:
        self.disconnect()

    # -- moving -------------------------------------------------------------- #
    def motor(
        self,
        number: int,
        direction: str = "forward",
        speed: int = 5,
        seconds: float | None = None,
    ) -> None:
        """Turn one motor (``number`` is 1, 2, or 3).

        ``direction`` is ``"forward"`` or ``"backward"``. If you give
        ``seconds``, the motor runs for that long and then stops. Handy for
        working out which motor is which (see :meth:`identify_motors`).
        """
        self._require_connection()
        port = motor_from_number(number)
        self._run(self._robot.run_motor(port, _direction_value(direction), _clamp_speed(speed)))
        if seconds is not None:
            self.wait(seconds)
            self._run(self._robot.stop_motor(port))

    def _drive(
        self, forward_left: bool, forward_right: bool, seconds: float | None, speed: int
    ) -> None:
        """Run the two wheel motors together (used by forward/back/turns)."""
        self._require_connection()
        spd = _clamp_speed(speed)
        left_motor, left_dir, right_motor, right_dir = drive_directions(
            self._profile, forward_left, forward_right
        )
        self._run(self._robot.run_motor(left_motor, left_dir, spd))
        self._run(self._robot.run_motor(right_motor, right_dir, spd))
        if seconds is not None:
            self.wait(seconds)
            self.stop()

    def forward(self, seconds: float | None = None, speed: int = 5) -> None:
        """Drive forward. Add ``seconds`` to go for a while then stop."""
        self._drive(True, True, seconds, speed)

    def backward(self, seconds: float | None = None, speed: int = 5) -> None:
        """Drive backward."""
        self._drive(False, False, seconds, speed)

    def turn_left(self, seconds: float | None = None, speed: int = 5) -> None:
        """Spin to the left."""
        self._drive(False, True, seconds, speed)

    def turn_right(self, seconds: float | None = None, speed: int = 5) -> None:
        """Spin to the right."""
        self._drive(True, False, seconds, speed)

    def stop(self) -> None:
        """Stop all the motors right now."""
        self._require_connection()
        self._run(self._robot.stop_all_motors())

    # -- lights -------------------------------------------------------------- #
    def color(self, color: str) -> None:
        """Make all the lights a color, like ``robot.color("purple")``.

        Colors: off, red, orange, yellow, green, cyan, blue, purple, white.
        """
        self._require_connection()
        self._run(self._robot.all_leds(_color_value(color)))

    def lights_off(self) -> None:
        """Turn all the lights off."""
        self.color("off")

    # -- waiting ------------------------------------------------------------- #
    def wait(self, seconds: float) -> None:
        """Wait for a number of seconds before doing the next thing."""
        self._run(asyncio.sleep(max(0.0, float(seconds))))

    # -- calibration helpers ------------------------------------------------- #
    def identify_motors(self, seconds: float = 1.2, speed: int = 5) -> None:
        """Run each motor (1, 2, 3) on its own so you can see which is which.

        Watch the robot: note which motor moves the left wheel and which moves
        the right wheel. Then set them with ``left_motor=`` / ``right_motor=``.
        """
        self._require_connection()
        self._say("Testing each motor one at a time. Watch which part moves!")
        for number in (1, 2, 3):
            self._say(f"  -> motor {number}")
            self.motor(number, "forward", speed=speed, seconds=seconds)
            self.wait(0.6)
        self._say("Done. Which motor moved the left wheel, and which the right?")

    def test_drive(self, seconds: float = 1.5, speed: int = 5) -> None:
        """Drive forward, back, left, then right, announcing each move.

        Use this to check the driving directions are right for your build.
        """
        self._require_connection()
        self._say("Checking driving directions. Watch the robot:")
        self._say("  -> FORWARD (should move away from you)")
        self.forward(seconds, speed)
        self.wait(0.5)
        self._say("  -> BACKWARD (should come back toward you)")
        self.backward(seconds, speed)
        self.wait(0.5)
        self._say("  -> TURN LEFT (should spin left in place)")
        self.turn_left(seconds, speed)
        self.wait(0.5)
        self._say("  -> TURN RIGHT (should spin right in place)")
        self.turn_right(seconds, speed)
        self._say("If any of those were wrong, see docs/EASY.md to fix it.")

    def show_setup(self) -> None:
        """Print the current wheel setup and how to recreate it in code."""
        p = self._profile
        left_num = {Motor.M1: 1, Motor.M2: 2, Motor.M3: 3}[p.left_motor]
        right_num = {Motor.M1: 1, Motor.M2: 2, Motor.M3: 3}[p.right_motor]
        self._say(
            f"{p.name} (product='{p.product}')\n"
            f"  left wheel  = motor {left_num}, forward = {p.left_forward.name}\n"
            f"  right wheel = motor {right_num}, forward = {p.right_forward.name}\n"
            f"  calibrated  = {p.calibrated}"
        )
