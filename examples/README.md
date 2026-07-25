# Examples

Small, self-contained programs you can run directly. Turn a robot on nearby,
then run any of them with `python examples/<name>.py`. Most default to Robot J —
pass a different product by editing the `Robot()` call (e.g. `Robot(product="s")`).

| File | What it does |
|------|--------------|
| [`kids_first_program.py`](kids_first_program.py) | The gentlest intro: drive a little and blink some lights. |
| [`drive_square.py`](drive_square.py) | Drive in a square using a `for` loop. |
| [`rainbow.py`](rainbow.py) | Cycle the LEDs through every color. |
| [`police_lights.py`](police_lights.py) | Flashing red-and-blue lights. |
| [`keyboard_drive.py`](keyboard_drive.py) | Drive from the keyboard (type a key + Enter). |
| [`joystick.py`](joystick.py) | Live single-key driving, no Enter needed. |
| [`autonomous_demo.py`](autonomous_demo.py) | The robot drives its own randomized patrol. |
| [`use_in_another_project.py`](use_in_another_project.py) | Using the full async API from your own code. |

New to this? Start with `kids_first_program.py` and the
[beginner guide](../docs/EASY.md).
