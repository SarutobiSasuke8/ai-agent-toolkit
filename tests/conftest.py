"""Shared fixtures that keep the test suite fully offline.

Every test runs with no API keys set and with outbound sockets blocked, so a
missed mock fails loudly instead of quietly calling a real service.
"""

from __future__ import annotations

import socket

import pytest


class NetworkBlockedError(RuntimeError):
    """Raised when a test tries to open a real network connection."""


@pytest.fixture(autouse=True)
def offline(monkeypatch: pytest.MonkeyPatch) -> None:
    """Remove API keys and block outbound network access for every test."""
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    def _blocked(*args, **kwargs):
        raise NetworkBlockedError("Network access is disabled in tests.")

    monkeypatch.setattr(socket.socket, "connect", _blocked)
    monkeypatch.setattr(socket, "create_connection", _blocked)
