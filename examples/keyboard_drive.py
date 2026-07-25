"""Drive the robot from the keyboard (type a key, then Enter).

    python examples/keyboard_drive.py

Keys:
    w = forward     s = backward
    a = turn left   d = turn right
    space = stop    r/g/b = red/green/blue light   o = lights off
    q = quit

This version reads a whole line, so it works in any terminal. For instant
single-key control (no Enter), see joystick.py.
"""

from apitor_ble.easy import Robot

STEP = 0.6  # seconds each move runs before stopping


def main() -> None:
    robot = Robot()
    robot.connect()
    print(__doc__)
    try:
        while True:
            key = input("> ").strip().lower()
            if key == "q":
                break
            elif key == "w":
                robot.forward(STEP)
            elif key == "s":
                robot.backward(STEP)
            elif key == "a":
                robot.turn_left(STEP)
            elif key == "d":
                robot.turn_right(STEP)
            elif key in ("", " ", "space"):
                robot.stop()
            elif key == "r":
                robot.color("red")
            elif key == "g":
                robot.color("green")
            elif key == "b":
                robot.color("blue")
            elif key == "o":
                robot.lights_off()
            else:
                print("  (unknown key)")
    except (KeyboardInterrupt, EOFError):
        pass
    finally:
        robot.stop()
        robot.disconnect()


if __name__ == "__main__":
    main()
