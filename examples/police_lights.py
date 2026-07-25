"""Flashing red-and-blue police lights.

    python examples/police_lights.py

Press Ctrl+C to stop.
"""

from apitor_ble.easy import Robot

FLASH = 0.15  # seconds per flash


def main() -> None:
    robot = Robot()
    robot.connect()
    try:
        print("Police lights! Press Ctrl+C to stop.")
        while True:
            for _ in range(3):  # a burst of red
                robot.color("red")
                robot.wait(FLASH)
                robot.lights_off()
                robot.wait(FLASH)
            for _ in range(3):  # a burst of blue
                robot.color("blue")
                robot.wait(FLASH)
                robot.lights_off()
                robot.wait(FLASH)
    except KeyboardInterrupt:
        pass
    finally:
        robot.lights_off()
        robot.disconnect()


if __name__ == "__main__":
    main()
