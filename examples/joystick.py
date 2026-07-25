"""Live single-key "joystick" driving — no Enter needed.

    python examples/joystick.py

Hold-and-tap the keys to drive in real time:
    w = forward   s = backward   a = turn left   d = turn right
    space = stop  r/g/b = lights  o = off  q = quit

Each key press drives for a short moment. Uses a tiny cross-platform
single-character reader (``msvcrt`` on Windows, ``termios`` on macOS/Linux).
"""

import sys

from apitor_ble.easy import Robot

STEP = 0.4  # seconds each key press drives


def _read_key() -> str:
    """Read one keypress without waiting for Enter (cross-platform)."""
    try:  # Windows
        import msvcrt

        return msvcrt.getwch()
    except ImportError:  # macOS / Linux
        import termios
        import tty

        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            return sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)


def main() -> None:
    robot = Robot()
    robot.connect()
    print(__doc__)
    try:
        while True:
            key = _read_key().lower()
            if key in ("q", "\x03"):  # q or Ctrl+C
                break
            elif key == "w":
                robot.forward(STEP)
            elif key == "s":
                robot.backward(STEP)
            elif key == "a":
                robot.turn_left(STEP)
            elif key == "d":
                robot.turn_right(STEP)
            elif key == " ":
                robot.stop()
            elif key == "r":
                robot.color("red")
            elif key == "g":
                robot.color("green")
            elif key == "b":
                robot.color("blue")
            elif key == "o":
                robot.lights_off()
    finally:
        robot.stop()
        robot.disconnect()


if __name__ == "__main__":
    main()
