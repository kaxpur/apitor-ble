# The easy Robot API (for beginners) 🤖

This is the simplest way to control an **Apitor robot** with Python. It's
made for people who are just starting to learn programming. There's no
Bluetooth setup, no `async`/`await`, and no confusing symbols — you just tell
the robot what to do, one line at a time.

Robot J works out of the box. Other Apitor kits (Robot S, Q, R, X, and Wheels)
work too — see [Using a different robot](#using-a-different-robot) below.

## Your first program

Turn the robot on, put it near the computer, and run this:

```python
from apitor_ble.easy import Robot

robot = Robot()
robot.connect()

robot.forward(2)      # drive forward for 2 seconds
robot.color("blue")   # make the lights blue
robot.wait(1)         # wait 1 second
robot.lights_off()

robot.disconnect()
```

There's a ready-to-run copy in
[`examples/kids_first_program.py`](../examples/kids_first_program.py):

```bash
python examples/kids_first_program.py
```

## Steps to remember

1. **Make a robot:** `robot = Robot()`
2. **Connect:** `robot.connect()` — do this once, before anything else.
3. **Give commands** (below).
4. **Say goodbye:** `robot.disconnect()` when you're done.

## Moving around

Each of these can take a number of **seconds**. If you give a number, the robot
moves for that long and then stops by itself.

```python
robot.forward(2)      # forward for 2 seconds
robot.backward(2)     # backward for 2 seconds
robot.turn_left(1)    # turn left for 1 second
robot.turn_right(1)   # turn right for 1 second
robot.stop()          # stop right now
```

You can also go faster or slower with `speed` (1 = slow, 10 = fast):

```python
robot.forward(2, speed=10)   # zoom!
robot.forward(2, speed=2)    # slow and steady
```

Want to control just one motor? Motors are numbered 1, 2, and 3:

```python
robot.motor(1, "forward", speed=5, seconds=2)
robot.motor(2, "backward")
```

## Lights

```python
robot.color("red")
robot.color("purple")
robot.lights_off()
```

The colors you can use are:
**off, red, orange, yellow, green, cyan, blue, purple, white**.

## Waiting

```python
robot.wait(1.5)   # do nothing for 1.5 seconds
```

## Tips for grown-ups helping out

- If **"forward" makes the robot go backward**, that just means the motors are
  plugged in the other way. You can swap the motor plugs, or use `backward`
  instead — both are fine.
- `forward` / `backward` / `turn_left` / `turn_right` drive **motor 1 and
  motor 2** together (the two wheels). Motor 3, if your model has one, drives an
  accessory (a drill, an arm) — control it with `robot.motor(3, ...)`.
- If the robot can't be found, make sure it's **turned on**, **charged**, and
  **not already connected to a phone or another computer** (it can only talk to
  one at a time).
- Want to hide the friendly messages? Use `Robot(quiet=True)`.

## Using a different robot

Every Apitor kit uses the same commands — just tell `Robot` which one:

```python
robot = Robot(product="s")   # "j" (default), "s", "q", "r", "x", or "w" (Wheels)
```

Connecting and the lights work the same on every robot. **Driving** is the only
thing that can differ, because which motor is the left/right wheel — and which
way is "forward" — depends on how the kit was physically built. Robot J's
directions are set from a real robot; the others start from the official app's
standard-build values and may need a quick check.

## Setting up a different robot

If forward, backward, or the turns come out wrong, you can fix them **without
editing any library code**. You watch the robot and adjust a couple of settings.

**Step 1 — see which motor is which wheel.** Build any driving model, then:

```python
robot = Robot(product="s")
robot.connect()
robot.identify_motors()      # runs motor 1, then 2, then 3, one at a time
robot.disconnect()
```

Note which motor number spins the **left** wheel and which spins the **right**.

**Step 2 — check the driving directions.**

```python
robot = Robot(product="s")
robot.connect()
robot.test_drive()           # forward, backward, left, right (announced)
robot.disconnect()
```

**Step 3 — fix whatever was wrong.** Pass these options to `Robot(...)`:

| What you saw | Fix |
|--------------|-----|
| Left and right wheels are swapped | `left_motor=2, right_motor=1` (use your numbers) |
| Forward and backward are swapped | `flip_left=True, flip_right=True` |
| It spins instead of driving straight | flip just **one** wheel: `flip_left=True` |
| Turns go the wrong way | swap the wheels: `left_motor=..., right_motor=...` |

```python
robot = Robot(product="s", flip_left=True)   # example
robot.connect()
robot.test_drive()                            # check again
```

Repeat step 3 until forward is forward. Then `robot.show_setup()` prints your
settings so you can save them. For the exact motor directions the official app
uses for **every** buildable model, see [ROBOTS.md](ROBOTS.md).

## When you're ready for more

This easy API sits on top of the full [`apitor_ble`](USAGE.md) library. When
you want motor-by-motor control, sensor notifications, or the raw protocol,
that's the next step up.
