"""Exception hierarchy for :mod:`apitor_ble`.

All library-specific errors derive from :class:`ApitorError`, so callers can
catch everything with a single ``except ApitorError``. More specific subclasses
let you handle particular failures (discovery, connection, authorization,
protocol decoding) individually.

``ApitorError`` subclasses :class:`RuntimeError` for backwards compatibility with
earlier releases where it was defined that way.
"""

from __future__ import annotations


class ApitorError(RuntimeError):
    """Base class for all errors raised by :mod:`apitor_ble`."""


class DiscoveryError(ApitorError):
    """No matching robot was found while scanning."""


class ConnectionError(ApitorError):
    """A BLE connection could not be established or was lost.

    Note: this intentionally shadows the built-in ``ConnectionError`` within the
    :mod:`apitor_ble` namespace; import it explicitly if you need the builtin.
    """


class AuthorizationError(ApitorError):
    """The authorization ("password") handshake failed."""


class ProtocolError(ApitorError):
    """A frame could not be built or decoded because it was malformed."""


__all__ = [
    "ApitorError",
    "DiscoveryError",
    "ConnectionError",
    "AuthorizationError",
    "ProtocolError",
]
