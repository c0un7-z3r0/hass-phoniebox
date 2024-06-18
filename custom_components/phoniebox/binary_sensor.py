"""Binary sensor platform for phoniebox."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.core import HomeAssistant, callback
from homeassistant.util import slugify

from .const import (
    BOOLEAN_SENSORS,
    CONF_PHONIEBOX_NAME,
    DOMAIN,
    LOGGER,
    TOPIC_LENGTH_PLAYER_STATE,
)
from .entity import PhonieboxEntity
from .utils import string_to_bool

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
    """Set binary_sensor platform up."""
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

            if sensor.name not in store:
                sensor.hass = hass
                sensor.set_state(value=string_to_bool(str(msg.payload)))
                store[sensor.name] = sensor
                LOGGER.debug(
                    "Registering binary sensor %(name)s", {"name": sensor.name}
                )
                async_add_devices(new_entities=(sensor,), update_before_add=True)
            else:
                store[sensor.name].set_state(value=string_to_bool(str(msg.payload)))
                store[sensor.name].async_schedule_update_ha_state()

    await coordinator.mqtt_client.async_subscribe("#", received_msg)


def _slug(name: str, phoniebox_name: str) -> str:
    return f"binary_sensor.phoniebox_{phoniebox_name}_{slugify(name)}"


class BinaryPhonieboxSensor(PhonieboxEntity, BinarySensorEntity):
    """phoniebox binary_sensor class."""

    _attr_should_poll = False

    def __init__(
        self,
        config_entry: ConfigEntry,
        name: str,
        coordinator: DataCoordinator,
        device_class: BinarySensorDeviceClass | None = None,
    ) -> None:
        """Init the sensor."""
        LOGGER.info("---->")
        super().__init__(config_entry, coordinator)
        self.entity_id = _slug(name, config_entry.data[CONF_PHONIEBOX_NAME])
        self._attr_name = name
        self._attr_device_class = device_class

    def set_event(self, event: Any) -> None:  # pylint: disable=unused-argument  # noqa: ARG002
        """Update the binary sensor with the most recent value."""
        return

    def set_state(self, *, value: bool) -> None:
        """Update the binary sensor with the most recent value."""
        if self._attr_is_on == value:
            return
        LOGGER.debug(
            "Updating binary sensor %(name)s to -> %(value)s",
            {"name": self.name, "value": value},
        )
        self._attr_is_on = value
