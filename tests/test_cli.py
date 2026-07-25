"""Tests for the CLI argument parsing (no hardware, no connection)."""

import pytest

from apitor_ble import cli


def test_all_commands_registered():
    assert set(cli.COMMANDS) == {"scan", "demo", "listen", "drive"}


def test_parser_defaults():
    args = cli.build_parser().parse_args(["scan"])
    assert args.command == "scan"
    assert args.product == "j"
    assert args.address is None
    assert args.timeout == 10.0
    assert args.verbose is False


def test_parser_options():
    args = cli.build_parser().parse_args(
        ["demo", "--product", "s", "--address", "AA:BB", "--timeout", "3", "--verbose"]
    )
    assert args.command == "demo"
    assert args.product == "s"
    assert args.address == "AA:BB"
    assert args.timeout == 3.0
    assert args.verbose is True


def test_unknown_command_rejected():
    with pytest.raises(SystemExit):
        cli.build_parser().parse_args(["fly"])
