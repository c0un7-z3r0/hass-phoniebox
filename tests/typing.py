"""Typing helpers for Home Assistant tests."""

from __future__ import annotations

from unittest.mock import MagicMock

type MqttMockHAClient = MagicMock  # type: ignore[valid-type]
"""MagicMock for `homeassistant.components.mqtt.MQTT`."""
