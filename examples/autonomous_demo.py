"""A tiny "autonomous" robot: it drives its own randomized patrol.

    python examples/autonomous_demo.py

No steering from you — the program picks each move at random and shows a matching
light. It runs for a set number of moves (or until you press Ctrl+C).
"""

import random

from apitor_ble.easy import Robot

MOVES = 12  # how many random moves to make

# (method name, seconds, light color) choices the robot picks between.
CHOICES = [
    ("forward", 1.5, "green"),
    ("forward", 2.0, "green"),
    ("turn_left", 0.6, "yellow"),
    ("turn_right", 0.6, "yellow"),
    ("backward", 1.0, "red"),
]


def main() -> None:
    robot = Robot()
    robot.connect()
    try:
        print(f"Patrolling on my own for {MOVES} moves. Press Ctrl+C to stop.")
        for step in range(MOVES):
            name, seconds, color = random.choice(CHOICES)
            print(f"  {step + 1}/{MOVES}: {name}({seconds})")
            robot.color(color)
            getattr(robot, name)(seconds)
            robot.wait(0.3)
        print("Patrol complete.")
    except KeyboardInterrupt:
        pass
    finally:
        robot.lights_off()
        robot.disconnect()


if __name__ == "__main__":
    main()
