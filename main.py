#!/usr/bin/env python3
"""Backwards-compatible launcher for the apitor CLI.

The CLI now lives in :mod:`apitor_ble.cli` and installs as the ``apitor``
console command (``apitor scan``, ``apitor demo``, ...). This shim keeps the
older ``python main.py <command>`` invocation working.
"""

from apitor_ble.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
