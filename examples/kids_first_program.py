"""My first robot program! 🤖

Run it like this:

    python examples/kids_first_program.py

Make sure your Apitor Robot J is turned on and close to the computer.
Try changing the numbers and colors and see what happens!
"""

from apitor_ble.easy import Robot

# 1. Make a robot and connect to it.
robot = Robot()
robot.connect()

# 2. Drive around.
robot.forward(2)      # go forward for 2 seconds
robot.turn_right(1)   # turn right for 1 second
robot.backward(2)     # go backward for 2 seconds

# 3. Play with the lights.
robot.color("red")
robot.wait(1)         # wait 1 second
robot.color("green")
robot.wait(1)
robot.color("blue")
robot.wait(1)
robot.lights_off()

# 4. All done — say goodbye.
robot.disconnect()
