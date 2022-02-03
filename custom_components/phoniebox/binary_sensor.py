"""Binary sensor platform for phoniebox."""
from __future__ import annotations

import logging

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.config_entries import ConfigEntries

from .const import BOOLEAN_SENSORS, CONF_PHONIEBOX_NAME, DOMAIN, NAME, VERSION
from .entity import PhonieboxEntity
from .sensor import _slug
from .utils import string_to_bool

_LOGGER: logging.Logger = logging.getLogger(__package__)


def find_device_class(domain: str) -> BinarySensorDeviceClass | None:
    """
    Based on the domain find the corresponding device class
    """
    return None


def discover_sensors(topic, entry, coordinator):
    """
    Based on the topic and entry create the correct binary sensor
    """
    parts = topic.split("/")
    domain = parts[2] if len(parts) == 3 else parts[1]

    if domain not in BOOLEAN_SENSORS:
        return

    device_class = find_device_class(domain)

    return BinaryPhonieboxSensor(entry, domain, coordinator, device_class )


async def async_setup_entry(hass, entry, async_add_devices):
    """Setup binary_sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    def received_msg(msg):
        sensors = discover_sensors(msg.topic, entry, coordinator)
        store = coordinator.sensors

        if not sensors:
            return

        if isinstance(sensors, BinaryPhonieboxSensor):
            sensors = (sensors,)

        for sensor in sensors:
            if sensor.name not in store:
                sensor.hass = hass
                sensor.set_state(string_to_bool(msg.payload))
                store[sensor.name] = sensor
                _LOGGER.debug(
                    "Registering sensor %(name)s",
                    {"name": sensor.name},
                )
                async_add_devices((sensor,), True)
            else:
                store[sensor.name].set_state(string_to_bool(msg.payload))

    await coordinator.mqtt_client.async_subscribe("#", received_msg)


class BinaryPhonieboxSensor(PhonieboxEntity, BinarySensorEntity):
    """phoniebox binary_sensor class."""

    _attr_should_poll = False

    def __init__(
        self,
        config_entry: ConfigEntries,
        name: str,
        coordinator,
        device_class: BinarySensorDeviceClass = None,
    ):
        super().__init__(config_entry, coordinator)
        self.entity_id = _slug(name, config_entry.data[CONF_PHONIEBOX_NAME])
        self._attr_name = name
        self._attr_device_class = device_class

    def set_state(self, value: bool) -> None:
        """Update the binary sensor with the most recent value."""
        self._attr_is_on = value
        self.async_write_ha_state()
