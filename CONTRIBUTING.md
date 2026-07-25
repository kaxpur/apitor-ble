# Contributing to apitor-ble

Thanks for your interest! This project is an unofficial, community-maintained
library for driving Apitor toy robots over Bluetooth LE. Contributions from
educators, students, and tinkerers are very welcome.

## Ways to help

- **Calibrate a robot.** The most valuable contribution right now: build one of
  the models in [`docs/ROBOTS.md`](docs/ROBOTS.md), run the calibration steps in
  [`docs/EASY.md`](docs/EASY.md#setting-up-a-different-robot), and tell us the
  settings that made *forward* actually go forward. See "Reporting a verified
  robot" below.
- **Improve the docs** — especially the beginner ([EASY.md](docs/EASY.md)) and
  teacher ([TEACHERS.md](docs/TEACHERS.md)) guides.
- **Fix bugs or add features** in the protocol/driver layers.

## Development setup

```bash
git clone <your-fork-url>
cd apitor-ble
pip install -e ".[dev]"     # library + bleak + pytest
pytest                       # the protocol/profile/easy tests need no hardware
```

Python 3.9+ and a Bluetooth LE adapter (for hardware work). The protocol,
profile, and easy-layer helper tests are all hardware-free and must stay that
way — they're what lets anyone run `pytest` without a robot.

## Project layout

- `apitor_ble/protocol.py` — pure byte-level protocol, no I/O.
- `apitor_ble/sensor.py` — notification decoding.
- `apitor_ble/robot.py` — async BLE driver (`bleak`).
- `apitor_ble/easy.py` — the beginner-friendly synchronous API.
- `apitor_ble/profiles.py` — per-robot driving profiles.
- `docs/` — protocol reference, usage, beginner + teacher guides, robot tables.
- `tests/` — hardware-free tests.

## Reporting a verified robot

If you calibrate a robot on real hardware, please open an issue or PR with:

1. The **product** (`j`/`s`/`q`/`r`/`x`/`w`) and the **model** you built
   (e.g. "Robot S — RC Car").
2. The working settings, from `robot.show_setup()` — the left/right motor
   numbers and each wheel's forward direction.
3. Whether `robot.test_drive()` came out correct (forward/back/left/right).

That lets us mark a profile `calibrated=True` and help the next person. When a
profile is confirmed, update the default in `apitor_ble/profiles.py` and add a
test in `tests/test_profiles.py` that locks in the mapping.

## Style & guidelines

- Match the surrounding code: type hints, short docstrings, no new runtime
  dependencies beyond `bleak`.
- Keep the `easy` API beginner-first — plain English, friendly errors, no
  `async` leaking out.
- Add or update tests for anything testable without hardware.
- This project is not affiliated with Apitor. Only add functionality for
  interoperability with hardware people own.

## License

By contributing you agree that your contributions are licensed under the
project's [MIT License](LICENSE).
