# Changelog

All notable changes to this project are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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

[Unreleased]: https://github.com/kaxpur/apitor-ble/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/kaxpur/apitor-ble/releases/tag/v0.1.0
