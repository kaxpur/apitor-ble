# Apitor robots in the classroom — a teacher's quickstart

A short guide to using `apitor-ble` to teach beginner programming with Apitor
robots. No prior robotics or Bluetooth knowledge needed. Students write a few
lines of ordinary Python and the robot moves.

> Unofficial project, not affiliated with Apitor. For use with robots you own.

## What you need

- One or more **Apitor robots** (Robot J, S, Q, R, X, or Wheels), charged and
  built into a driving model.
- A computer per group with **Bluetooth** and **Python 3.10+**.
- 10 minutes to set up once.

## Installing for Python development

You install the library **once per computer**, from the **terminal** (not from
inside Python). Pick the section that matches the machine.

> ⚠️ **`pip` goes in the terminal, not the `>>>` prompt.** If you type
> `pip install ...` after Python's `>>>` you'll get `SyntaxError`. Run it in the
> Command Prompt / Terminal instead. (`import apitor_ble` is the part that goes
> *inside* Python.)

### Windows / macOS

```bash
pip install apitor-ble
# if "pip" isn't found:  py -m pip install apitor-ble   (Windows)
#                        python3 -m pip install apitor-ble   (macOS)
```

### Raspberry Pi / Linux (use a virtual environment)

Debian-based systems (including Raspberry Pi OS) protect the system Python, so a
plain `pip install` fails with **"externally-managed-environment"**. Make a
project **virtual environment** (a private sandbox) once, and install into it:

```bash
cd ~/my-robot-project            # your project folder
python3 -m venv .venv            # create the sandbox (once)
source .venv/bin/activate        # enter it — prompt shows (.venv)
pip install apitor-ble           # now this works
```

Each new terminal, run `source .venv/bin/activate` again before working;
`deactivate` leaves it. Add `apitor-ble` to a `requirements.txt` so students can
recreate it with `pip install -r requirements.txt`.

### Using Thonny (the default Raspberry Pi editor)

Thonny works great — you do **not** need IDLE. But out of the box it runs the
**system Python**, which won't see the library you installed into `.venv`. Point
Thonny at your virtual environment once:

1. **Tools → Options → Interpreter**
2. Under "Which interpreter…", choose **Alternative Python 3 interpreter or
   virtual environment**.
3. For "Python executable", browse to your venv's Python, e.g.
   `~/my-robot-project/.venv/bin/python3`.
4. Click **OK**. The Shell pane restarts showing that path.

Now pressing **Run (F5)** uses the venv, and `from apitor_ble.easy import Robot`
works. (The tell-tale sign it's on the wrong interpreter: `ModuleNotFoundError:
No module named 'apitor_ble'` even though you installed it.)

### Check it works

Turn a robot on nearby and run (from the terminal, or Run in Thonny):

```python
from apitor_ble.easy import Robot
r = Robot(); r.connect(); r.color("green"); r.wait(1); r.lights_off(); r.disconnect()
```

If the lights flash green, you're ready.

## The very first lesson

Have students create `my_robot.py`:

```python
from apitor_ble.easy import Robot

robot = Robot()          # use Robot(product="s") etc. for other kits
robot.connect()

robot.forward(2)         # drive forward for 2 seconds
robot.color("blue")      # lights blue
robot.wait(1)
robot.lights_off()

robot.disconnect()
```

Run it with `python my_robot.py`. Then let them change the numbers and colors.
The full beginner reference is [EASY.md](EASY.md); a ready-to-run example is
[`examples/first_program.py`](../examples/first_program.py).

The commands students have:

- **Move:** `forward`, `backward`, `turn_left`, `turn_right`, `stop`
  (each takes seconds, e.g. `robot.forward(2)`, and an optional `speed=1..10`).
- **Lights:** `robot.color("red")` … (off, red, orange, yellow, green, cyan,
  blue, purple, white), `robot.lights_off()`.
- **Wait:** `robot.wait(1.5)`.
- **One motor:** `robot.motor(1, "forward", seconds=2)`.

## Lesson ideas (increasing difficulty)

1. **Traffic lights** — cycle red → yellow → green with `wait`s.
2. **Drive a square** — repeat forward + turn four times (great intro to `for`
   loops: `for i in range(4): ...`).
3. **Dance routine** — a sequence students design, set to counts of seconds.
4. **Functions** — have them write `def wiggle(): ...` and call it.
5. **Obstacle course** — measure real distances, tune `seconds`/`speed`.

## Before class: calibrate each robot once

Driving directions depend on how a kit was physically built, so check each robot
once (do this yourself, or make it the students' first investigation):

```python
robot = Robot()          # or Robot(product="s")
robot.connect()
robot.test_drive()       # announces forward, backward, left, right — watch it
robot.disconnect()
```

If a move is wrong, fix it with a setting and re-check — see the table in
[EASY.md → Setting up a different robot](EASY.md#setting-up-a-different-robot).
Once it's right, `robot.show_setup()` prints the settings; write them on the
robot's box, e.g. `Robot(product="s", flip_left=True)`.

Robot J is pre-set. Other kits start from the official app's values and may need
a flip.

## Classroom tips

- **One connection at a time.** A robot talks to a single device — if it won't
  connect, another computer (or the Apitor phone app) probably has it. Close the
  other connection.
- **Name your robots.** With several in a room, connect to a specific one by its
  Bluetooth address: `Robot(address="EB:28:75:C0:66:07")`. Find addresses with
  `python main.py scan`.
- **Battery.** "Won't move" or "moves weakly" is often a low battery — the robot
  reports low power, and moves need roughly `speed=4`+ to overcome friction.
- **Keep runs short.** Motors keep going until stopped; the timed calls
  (`forward(2)`) stop automatically, which is safest for beginners.
- **Quiet mode.** `Robot(quiet=True)` hides the friendly status messages if you
  want clean output.

## Troubleshooting

| Problem | Fix |
|---------|-----|
| "I couldn't find your robot" | Turn it on; make sure no other device/app is connected; keep it close. |
| Forward goes backward / it spins | Calibrate — see above. |
| A color name errors | Use one of the nine listed color names. |
| Weak or no movement | Charge the battery; raise `speed`. |
| Unicode/emoji error in a terminal | Already handled by the library; update to the latest version if you see one. |

## Going further

When students outgrow the easy API, the full asynchronous library
([USAGE.md](USAGE.md)) exposes per-motor control, sensor notifications, and the
raw protocol ([PROTOCOL.md](PROTOCOL.md)).
