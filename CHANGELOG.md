# Changelog

All notable changes to this project are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.1] - 2026-07-26

### Added
- Published to PyPI: `pip install apitor-ble`. README now shows PyPI + Python
  version badges and leads with the PyPI install.
- `release.yml` workflow publishes to PyPI via Trusted Publishing (OIDC).

### Changed
- Docs use inclusive "students"/"instructors" wording instead of "kids"/
  "grown-ups" (the library suits learners of any age). Renamed
  `examples/kids_first_program.py` to `examples/first_program.py`.
- Bumped GitHub Actions to current major versions (Node 24) to clear the
  Node 20 deprecation warnings.

## [0.2.0] - 2026-07-25

Packaging, tooling, and code-quality pass to make the project PyPI-ready. No
breaking API changes.

### Added
- **Console entry point**: installs an `apitor` command (`apitor scan|demo|
  listen|drive`) via `console_scripts`. `python main.py <command>` still works.
- **`apitor_ble.constants`**: all wire values as named constants (no more magic
  numbers like `0x55` / `0x03` scattered through the code).
- **`apitor_ble.exceptions`**: `ApitorError` base plus `DiscoveryError`,
  `ConnectionError`, `AuthorizationError`, and `ProtocolError`; the driver now
  raises the specific type (all still catchable as `ApitorError`).
- **GitHub Actions CI** running Ruff, Black, and pytest on Python 3.10-3.13.
- **PEP 561 typing marker** (`py.typed`) — the package ships as typed.
- More example programs: `drive_square`, `rainbow`, `police_lights`,
  `keyboard_drive`, `joystick`, `autonomous_demo`, plus an examples index.
- Packet diagrams in `docs/PROTOCOL.md` showing the meaning of every byte.
- Complete package metadata in `pyproject.toml`: classifiers, project URLs.
- README: badges, "Why?", "Demo" (placeholders), "Roadmap", and "Disclaimer".
- Tests for the constants, exceptions, and CLI parsing (54 tests total).

### Changed
- Require Python 3.10+ (was 3.9+), consistent across README, `pyproject.toml`,
  and `docs/USAGE.md`.
- `protocol.py` and `sensor.py` now build every frame from `constants.py`.
- The CLI owns all user-facing terminal output; core library modules use
  `logging` only. (The beginner `easy` layer still prints friendly messages by
  design, silenceable with `Robot(quiet=True)`.)
- Codebase formatted with Black and linted with Ruff.

## [0.1.0] - 2026-07-25

First public release.

### Added
- **Beginner "easy mode" API** (`apitor_ble.easy.Robot`): a synchronous,
  plain-English wrapper that hides Bluetooth and `async`/`await`. Movement
  (`forward`, `backward`, `turn_left`, `turn_right`, `stop`), timed moves,
  per-motor control, LED colors, and `wait`, with friendly error messages.
- **Multi-robot support** via `Robot(product=...)` for all Apitor BLE kits
  (Robot J, S, Q, R, X, and Wheels).
- **Per-robot driving profiles** (`apitor_ble.profiles`) with mappings derived
  from the official app configuration, plus calibration options
  (`left_motor`, `right_motor`, `flip_left`, `flip_right`) and helpers
  (`identify_motors`, `test_drive`, `show_setup`) to set up a specific build
  without editing library code.
- **Async core library** (`apitor_ble.ApitorRobot`): scan/discover, connect with
  the authorization handshake, motor and LED control, raw frame access, and
  notification callbacks (built on `bleak`).
- **Pure protocol layer** (`apitor_ble.protocol`) and notification decoding
  (`apitor_ble.sensor`) with hardware-free unit tests.
- **CLI** (`main.py`): `scan`, `demo`, `listen`, and `drive`.
- **Docs**: protocol reference (`docs/PROTOCOL.md`), usage (`docs/USAGE.md`),
  beginner guide (`docs/EASY.md`), official per-model motor tables
  (`docs/ROBOTS.md`), and a classroom quickstart (`docs/TEACHERS.md`).
- Project scaffolding: `LICENSE` (MIT), `CONTRIBUTING.md`, `.gitignore`.

### Notes
- Robot J's driving profile is confirmed against real hardware. The other
  products default to the official app's standard-build mappings and should be
  checked with the calibration steps in `docs/EASY.md`.
- Unofficial project; not affiliated with or endorsed by Apitor. The protocol
  was reverse-engineered for interoperability with hardware you own.

[Unreleased]: https://github.com/kaxpur/apitor-ble/compare/v0.2.1...HEAD
[0.2.1]: https://github.com/kaxpur/apitor-ble/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/kaxpur/apitor-ble/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/kaxpur/apitor-ble/releases/tag/v0.1.0
