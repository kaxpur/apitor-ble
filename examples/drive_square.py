"""Drive in a square: forward, turn, repeat four times.

    python examples/drive_square.py

A nice first taste of a `for` loop. Tune `SIDE` and `TURN` for your robot and
floor so it comes back roughly where it started.
"""

from apitor_ble.easy import Robot

SIDE = 2.0  # seconds driving forward along each side
TURN = 0.7  # seconds turning at each corner


def main() -> None:
    robot = Robot()
    robot.connect()
    try:
        for corner in range(4):
            print(f"Side {corner + 1} of 4")
            robot.forward(SIDE)
            robot.turn_right(TURN)
    finally:
        robot.stop()
        robot.disconnect()


if __name__ == "__main__":
    main()
