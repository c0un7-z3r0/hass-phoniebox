"""Data coordinator for phoniebox integration."""
from __future__ import annotations

from .mqtt_client import MqttClient


class DataCoordinator:
    """Class to manage date of the integration."""

    def __init__(self, mqtt_client: MqttClient) -> None:
        """Initialize."""
        self.platforms = []
        self.mqtt_client = mqtt_client
        self.sensors = {}
        self.switches = {}
        self.buttons = {}
        self.version = "unknown"
