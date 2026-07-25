"""Cycle the LEDs through every color, like a little rainbow.

python examples/rainbow.py
"""

from apitor_ble.easy import Robot

COLORS = ["red", "orange", "yellow", "green", "cyan", "blue", "purple", "white"]


def main() -> None:
    robot = Robot()
    robot.connect()
    try:
        for _ in range(3):  # three passes through the rainbow
            for color in COLORS:
                print(color)
                robot.color(color)
                robot.wait(0.4)
    finally:
        robot.lights_off()
        robot.disconnect()


if __name__ == "__main__":
    main()
