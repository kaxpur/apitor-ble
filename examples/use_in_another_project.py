"""Example: how another Python project imports and uses apitor_ble.

Install the library first (from the project root):

    pip install -e .

Then in your own project:
"""

import asyncio

from apitor_ble import ApitorRobot, Color, Direction, Motor


async def square_dance() -> None:
    """Connect to a Robot J and run a short scripted routine."""
    # Discover the first Robot J in range and connect. The `async with` block
    # guarantees the robot is disconnected (and motors stopped) on exit.
    robot = await ApitorRobot.discover(product="j", timeout=10.0)

    async with robot:
        await robot.all_leds(Color.CYAN)

        for _ in range(4):
            await robot.run_motor(Motor.M1, Direction.D1, speed=6)  # forward
            await asyncio.sleep(1.0)
            await robot.stop_all_motors()

            await robot.run_motor(Motor.M2, Direction.D1, speed=6)  # turn
            await asyncio.sleep(0.5)
            await robot.stop_all_motors()

        await robot.all_leds(Color.OFF)


if __name__ == "__main__":
    asyncio.run(square_dance())
