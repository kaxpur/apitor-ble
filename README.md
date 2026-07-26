# apitor-ble

[![PyPI](https://img.shields.io/pypi/v/apitor-ble.svg)](https://pypi.org/project/apitor-ble/)
[![Python versions](https://img.shields.io/pypi/pyversions/apitor-ble.svg)](https://pypi.org/project/apitor-ble/)
[![CI](https://github.com/kaxpur/apitor-ble/actions/workflows/ci.yml/badge.svg)](https://github.com/kaxpur/apitor-ble/actions/workflows/ci.yml)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Bluetooth LE](https://img.shields.io/badge/Bluetooth-LE-0082FC.svg?logo=bluetooth&logoColor=white)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Ruff](https://img.shields.io/badge/linter-ruff-D7FF64.svg)](https://github.com/astral-sh/ruff)

A small, dependency-light Python library for driving **Apitor** toy robots over
Bluetooth Low Energy — hardware tested using **Robot J** — plus a test/demo CLI and full
protocol documentation.

The protocol was reverse-engineered from the official *Apitor Kit* Android app.
See [`docs/PROTOCOL.md`](docs/PROTOCOL.md) for the byte-level details.

> ⚠️ Unofficial. Not affiliated with or endorsed by Apitor. For use with
> hardware you own, for interoperability and educational purposes.

## Why?

Apitor doesn't publish a public Bluetooth protocol for its robots, so there's no
official way to control them from your own code. This library fills that gap: the
protocol was independently reverse-engineered from the official app purely for
**interoperability** — so people can experiment, learn, teach, and build their
own robotics projects with hardware they already own.

## Features

- Async API built on [`bleak`](https://github.com/hbldh/bleak) (Windows/macOS/Linux).
- Scan + name-filter for Apitor devices, connect, and perform the required
  authorization handshake automatically.
- Motor control, LED control, raw frame access, and notification callbacks.
- Pure, hardware-free protocol layer (`apitor_ble.protocol`) with unit tests.

## Demo

See a real robot driven straight from Python — no app required.

<!-- Demo GIF goes here (e.g. keyboard driving via `python main.py drive`) -->

<!-- Robot J photo goes here -->

## Install

```bash
pip install apitor-ble
```

### From source

```bash
pip install -e .
```

### Requirements

- Python 3.10+
- A Bluetooth Low Energy adapter
- Supported on Windows, macOS, and Linux (via [`bleak`](https://github.com/hbldh/bleak))

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

Installing the package provides an `apitor` command:

```bash
apitor scan        # find nearby Robot J devices
apitor demo        # connect and run a motor + LED routine
apitor listen      # print incoming notification frames
apitor drive       # keyboard-driven live control

apitor demo --address AA:BB:CC:DD:EE:FF   # skip scanning
apitor scan --product s                   # a different Apitor product
apitor demo --verbose                     # log raw TX/RX frames
```

(The older `python main.py <command>` invocation still works too.)

## How it fits together

Each layer talks only to the one below it, so you can plug in at whatever level
you need:

```
Your code
│
├── easy.py        Beginner synchronous API  (uses profiles.py)
│
├── robot.py       Async BLE driver          (decodes via sensor.py)
│
├── protocol.py    Packet encoding
│
├── bleak          Bluetooth library
│
├── Bluetooth LE   Your computer's radio
│
└── Apitor Robot   Robot J / S / Q / R / X / Wheels
```

**Beginners** start at `easy.py`. **Advanced** users can drop straight to
`robot.py` for the full async API, or to `protocol.py` to build frames by hand.

## Project layout

```
apitor-ble/
├── apitor_ble/
│   ├── __init__.py        # public API
│   ├── protocol.py        # pure byte-level protocol (no I/O)
│   ├── sensor.py          # notification / telemetry decoding
│   ├── robot.py           # async BLE driver (bleak)
│   ├── profiles.py        # per-robot driving profiles
│   └── easy.py            # beginner-friendly synchronous API
├── main.py                # test / demo CLI
├── examples/
│   ├── use_in_another_project.py
│   └── first_program.py
├── tests/
│   ├── test_protocol.py   # hardware-free frame tests
│   ├── test_sensor.py     # notification decoding tests
│   ├── test_easy.py       # easy-API helper tests
│   └── test_profiles.py   # driving-profile tests
├── docs/
│   ├── PROTOCOL.md        # reverse-engineered protocol reference
│   ├── USAGE.md           # library + CLI usage guide
│   ├── EASY.md            # beginner guide + calibration steps
│   ├── ROBOTS.md          # official motor tables per model
│   └── TEACHERS.md        # classroom quickstart
├── CHANGELOG.md
├── CONTRIBUTING.md
├── LICENSE
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

| Item | Value | Notes |
|--------|-------|-------|
| Service | `0000f0ff-0000-1000-8000-00805f9b34fb` | GATT service |
| Write | `0000f001-...` | phone → robot, split into 20-byte chunks |
| Notify | `0000f002-...` | robot → phone |
| Name | `ApitorTJ...` | advertised name, case-insensitive |
| Auth | `55AA1120 436E354174675A4C4A7671723863447A` | send right after connect |
| Motor | `55AA03 <port> <dir> <speed>` | e.g. M1 fwd spd8 = `55AA03 06 01 08` |
| Stop | `55AA03 10 00 00` | stop all motors |
| LED | `55AA04 <index> <color> 00 00` | index 4 = all LEDs |

## Roadmap

Planned future improvements:

- Publish to PyPI
- Add GitHub Actions CI
- Add coverage reporting
- Support additional Apitor firmware revisions
- More example programs
- Additional classroom resources

## Changelog

See [`CHANGELOG.md`](CHANGELOG.md) for release notes.

## Contributing

Contributions are welcome — see [`CONTRIBUTING.md`](CONTRIBUTING.md). Especially
valuable:

- Testing on additional robots (and calibrating them on real hardware)
- Protocol verification
- Documentation improvements
- New example programs
- Bug reports

## Disclaimer

This project was independently reverse-engineered for interoperability.

It is not affiliated with, endorsed by, or supported by Apitor.

All trademarks belong to their respective owners.

## License

MIT — see [`LICENSE`](LICENSE).
