# apitor-ble

A small, dependency-light Python library for driving **Apitor** toy robots over
Bluetooth Low Energy — primarily **Robot J** — plus a test/demo CLI and full
protocol documentation.

The protocol was reverse-engineered from the official *Apitor Kit* Android app.
See [`docs/PROTOCOL.md`](docs/PROTOCOL.md) for the byte-level details.

> ⚠️ Unofficial. Not affiliated with or endorsed by Apitor. For use with
> hardware you own, for interoperability and educational purposes.

## Features

- Async API built on [`bleak`](https://github.com/hbldh/bleak) (Windows/macOS/Linux).
- Scan + name-filter for Apitor devices, connect, and perform the required
  authorization handshake automatically.
- Motor control, LED control, raw frame access, and notification callbacks.
- Pure, hardware-free protocol layer (`apitor_ble.protocol`) with unit tests.

## Install

```bash
pip install -e .        # library + bleak
```

## New to programming? Start here 🤖

There's a beginner-friendly API — no `async`, no Bluetooth setup, just plain
commands. See [`docs/EASY.md`](docs/EASY.md).

```python
from apitor_ble.easy import Robot

robot = Robot()            # Robot J by default; Robot(product="s") for others
robot.connect()

robot.forward(2)       # drive forward for 2 seconds
robot.color("blue")    # make the lights blue
robot.wait(1)
robot.lights_off()

robot.disconnect()
```

Works with every Apitor BLE kit (Robot J, S, Q, R, X, and Wheels). Driving
directions can be calibrated per build in a few lines — see
[Setting up a different robot](docs/EASY.md#setting-up-a-different-robot). For
the official motor tables of every buildable model, see
[`docs/ROBOTS.md`](docs/ROBOTS.md).

**Teaching with this?** There's a classroom quickstart with lesson ideas and
tips in [`docs/TEACHERS.md`](docs/TEACHERS.md).

## Use it in your project

```python
import asyncio
from apitor_ble import ApitorRobot, Motor, Direction, Color

async def main():
    robot = await ApitorRobot.discover(product="j")
    async with robot:
        await robot.run_motor(Motor.M1, Direction.D1, speed=8)
        await asyncio.sleep(2)
        await robot.stop_all_motors()
        await robot.all_leds(Color.BLUE)

asyncio.run(main())
```

A fuller example is in [`examples/use_in_another_project.py`](examples/use_in_another_project.py).

## Try it from the command line

```bash
python main.py scan        # find nearby Robot J devices
python main.py demo        # connect and run a motor + LED routine
python main.py listen      # print incoming notification frames
python main.py drive       # keyboard-driven live control
```

## Project layout

```
apitor-ble/
├── apitor_ble/
│   ├── __init__.py        # public API
│   ├── protocol.py        # pure byte-level protocol (no I/O)
│   └── robot.py           # async BLE driver (bleak)
├── main.py                # test / demo CLI
├── examples/
│   └── use_in_another_project.py
├── tests/
│   └── test_protocol.py   # hardware-free frame tests
├── docs/
│   ├── PROTOCOL.md        # reverse-engineered protocol reference
│   └── USAGE.md           # library + CLI usage guide
├── pyproject.toml
└── requirements.txt
```

## Tests

The protocol layer needs no hardware or `bleak`:

```bash
pip install pytest
pytest
```

## Robot J at a glance

```
Service : 0000f0ff-0000-1000-8000-00805f9b34fb
Write   : 0000f001-...   (split into 20-byte chunks)
Notify  : 0000f002-...
Name    : "ApitorTJ..."  (case-insensitive)
Auth    : 55AA1120 436E354174675A4C4A7671723863447A   (send right after connect)
Motor   : 55AA03 <port> <dir> <speed>       e.g. M1 fwd spd8 = 55AA03 06 01 08
Stop    : 55AA03 10 00 00
LED     : 55AA04 <index> <color> 00 00
```

## Changelog

See [`CHANGELOG.md`](CHANGELOG.md) for release notes.

## Contributing

Contributions are welcome — see [`CONTRIBUTING.md`](CONTRIBUTING.md). Calibrating
a robot on real hardware is especially valuable.

## License

MIT — see [`LICENSE`](LICENSE).
