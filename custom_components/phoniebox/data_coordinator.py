"""Data coordinator for phoniebox integration."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from custom_components.phoniebox.button import PhonieboxButton
    from custom_components.phoniebox.sensor import GenericPhonieboxSensor
    from custom_components.phoniebox.switch import PhonieboxBinarySwitch

    from .binary_sensor import BinaryPhonieboxSensor
    from .mqtt_client import MqttClient


class DataCoordinator:  # pylint: disable=too-few-public-methods
    """
    Class to manage data of the integration.

    This coordinator centralizes data management for the Phoniebox integration,
    maintaining references to all entities and the MQTT client.
    """

    def __init__(self, mqtt_client: MqttClient) -> None:
        """
        Initialize the data coordinator.

        Args:
        ----
            mqtt_client: The MQTT client instance for communication

        """
        # Use immutable approach for platforms list initialization
        self.platforms: list[str] = []
        self.mqtt_client = mqtt_client

        # Entity storage dictionaries
        self.sensors: dict[str, BinaryPhonieboxSensor | GenericPhonieboxSensor] = {}
        self.switches: dict[str, PhonieboxBinarySwitch] = {}
        self.buttons: dict[str, PhonieboxButton] = {}

        # Version information
        self.version = "unknown"
