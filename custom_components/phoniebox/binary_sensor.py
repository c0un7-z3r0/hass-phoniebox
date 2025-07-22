"""Binary sensor platform for phoniebox."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.core import HomeAssistant, callback

from .const import (
    BOOLEAN_SENSORS,
    CONF_PHONIEBOX_NAME,
    DOMAIN,
    LOGGER,
    TOPIC_LENGTH_PLAYER_STATE,
)
from .entity import PhonieboxEntity
from .utils import create_entity_slug, create_mqtt_context, handle_mqtt_entity_by_type

if TYPE_CHECKING:
    from homeassistant.components.mqtt.models import ReceiveMessage
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .data_coordinator import DataCoordinator


def discover_sensors(
    topic: str, entry: ConfigEntry, coordinator: DataCoordinator
) -> BinaryPhonieboxSensor | None:
    """Based on the topic and entry create the correct binary sensor."""
    parts = topic.split("/")
    domain = parts[2] if len(parts) == TOPIC_LENGTH_PLAYER_STATE else parts[1]

    if domain not in BOOLEAN_SENSORS:
        return None

    return BinaryPhonieboxSensor(entry, domain, coordinator, None)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_devices: AddEntitiesCallback,
) -> None:
    """
    Set binary_sensor platform up.

    Set up the binary sensor platform for the Phoniebox integration.
    This function initializes the binary sensors based on the configuration entry
    and subscribes to MQTT messages to receive updates for the sensors.

    Args:
    ----
        hass: The Home Assistant instance.
        config_entry: The configuration entry for the Phoniebox integration.
        async_add_devices: Callback to add devices to Home Assistant.

    """
    coordinator: DataCoordinator = hass.data[DOMAIN][config_entry.entry_id]
    LOGGER.debug("-----> Setup binary sensor")

    @callback
    def received_msg(msg: ReceiveMessage) -> None:
        LOGGER.debug("ReceiveMessage %(msg)s", {"msg": msg})
        sensors = discover_sensors(msg.topic, config_entry, coordinator)
        store = coordinator.sensors

        if not sensors:
            return

        sensor_list = (
            (sensors,) if isinstance(sensors, BinaryPhonieboxSensor) else sensors
        )

        for sensor in sensor_list:
            if not isinstance(sensor.name, str):
                continue

            context = create_mqtt_context(
                entity=sensor,
                store=store,
                hass=hass,
                msg_payload=msg.payload,
                async_add_entities_callback=async_add_devices,
            )
            handle_mqtt_entity_by_type(
                entity_type="binary_sensor",
                context=context,
                debug_logger=LOGGER,
            )

    await coordinator.mqtt_client.async_subscribe("#", received_msg)


def _slug(name: str, phoniebox_name: str) -> str:
    return create_entity_slug("binary_sensor", name, phoniebox_name)


class BinaryPhonieboxSensor(PhonieboxEntity, BinarySensorEntity):
    """
    Binary sensor entity for Phoniebox integration.

    This class represents a binary sensor that can be used to track boolean states
    in the Phoniebox system, such as play/pause status, connection state, or other
    on/off conditions.

    Attributes
    ----------
        _attr_should_poll: Set to False as the sensor is updated via events.
        entity_id: Unique identifier for the sensor entity.
        _attr_name: Display name of the sensor.
        _attr_device_class: Classification of the binary sensor type.
        _attr_is_on: Current boolean state of the sensor.

    Methods
    -------
        set_event: Placeholder method for handling events.
        set_state: Updates the sensor's boolean state and triggers HA updates.

    """

    _attr_should_poll = False

    def __init__(
        self,
        config_entry: ConfigEntry,
        name: str,
        coordinator: DataCoordinator,
        device_class: BinarySensorDeviceClass | None = None,
    ) -> None:
        """
        Init the binary sensor.

        Initializes the binary sensor with the given configuration entry, name,
        coordinator, and optional device class.

        Args:
        ----
            config_entry: The configuration entry for the Phoniebox integration.
            name: The name of the binary sensor.
            coordinator: The data coordinator managing the Phoniebox data.
            device_class: Optional device class for the binary sensor.

        """
        super().__init__(config_entry, coordinator)
        self.entity_id = _slug(name, config_entry.data[CONF_PHONIEBOX_NAME])
        self._attr_name = name
        self._attr_device_class = device_class

    def set_event(self, event: Any) -> None:  # pylint: disable=unused-argument  # noqa: ARG002
        """
        Update the binary sensor with the most recent value.

        This method is a placeholder and currently does not implement any functionality.
        """
        return

    def set_state(self, *, value: bool) -> None:
        """
        Update the binary sensor with the most recent value.

        This method updates the binary sensor's state and triggers Home Assistant
        to reflect the change. If the new value is the same as the current state,
        no action is taken to avoid unnecessary updates.

        Args:
        ----
            value: The new boolean state to set for the binary sensor.

        Raises:
        ------
            ValueError: If the value is not a boolean.

        If the value is not a boolean, this method will raise a ValueError.
        If the current state is already equal to the new value, no update is performed.

        """
        if self._attr_is_on == value:
            return
        LOGGER.debug(
            "Updating binary sensor %(name)s to -> %(value)s",
            {"name": self.name, "value": value},
        )
        self._attr_is_on = value
