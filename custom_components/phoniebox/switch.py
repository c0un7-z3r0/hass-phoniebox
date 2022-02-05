"""Switch platform for phoniebox."""
from __future__ import annotations

from abc import ABC
from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.helpers.entity import EntityCategory
from homeassistant.util import slugify

from .const import (
    BINARY_SWITCHES,
    CONF_PHONIEBOX_NAME,
    DOMAIN,
    NAME,
    PHONIEBOX_START,
    PHONIEBOX_STOP,
    VERSION, LOGGER,
)
from .entity import PhonieboxEntity
from .utils import string_to_bool


def discover_sensors(topic, entry, coordinator) -> PhonieboxBinarySwitch | None:
    """
    Based on the topic and entry create the correct binary switch
    """
    parts = topic.split("/")
    domain = parts[2] if len(parts) == 3 else parts[1]

    if domain not in BINARY_SWITCHES:
        return

    if domain in ["gpio", "rfid"]:
        return PhonieboxBinarySwitch(
            entry,
            coordinator,
            domain,
            domain,
            PHONIEBOX_START,
            PHONIEBOX_STOP,
            EntityCategory.CONFIG,
        )

    if domain == "random":
        return PhonieboxBinarySwitch(entry, coordinator, domain, "playershuffle")

    return PhonieboxBinarySwitch(entry, coordinator, domain, domain)


async def async_setup_entry(hass, entry, async_add_devices):
    """Setup binary_sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    def received_msg(msg):
        sensors = discover_sensors(msg.topic, entry, coordinator)
        store = coordinator.switches

        if not sensors:
            return

        if isinstance(sensors, PhonieboxBinarySwitch):
            sensors = (sensors,)

        for sensor in sensors:
            if sensor.name not in store:
                sensor.hass = hass
                sensor.set_state(string_to_bool(msg.payload))
                store[sensor.name] = sensor
                LOGGER.debug(
                    "Registering switch %(name)s",
                    {"name": sensor.name},
                )
                async_add_devices((sensor,), True)
            else:
                store[sensor.name].set_state(string_to_bool(msg.payload))

    await coordinator.mqtt_client.async_subscribe("#", received_msg)


def _slug(name, poniebox_name):
    return f"switch.phoniebox_{poniebox_name}_{slugify(name)}"


class PhonieboxBinarySwitch(PhonieboxEntity, SwitchEntity, ABC):
    """phoniebox switch class."""

    _attr_should_poll = False

    def __init__(
            self,
            config_entry,
            coordinator,
            name,
            mqtt_topic=None,
            mqtt_on_payload="",
            mqtt_off_payload="",
            entity_category=None,
    ):
        super().__init__(config_entry, coordinator)
        """Initialize the sensor."""
        self.entity_id = _slug(name, config_entry.data[CONF_PHONIEBOX_NAME])
        self._attr_name = name
        self._name = "switch_" + name
        self._mqtt_on_payload = mqtt_on_payload
        self._mqtt_off_payload = mqtt_off_payload
        self._mqtt_topic = mqtt_topic
        self._attr_entity_category = entity_category

    def set_state(self, value: bool) -> None:
        """Update the binary sensor with the most recent value."""
        self._attr_is_on = value
        self.async_write_ha_state()

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the entity on."""
        await self.mqtt_client.async_publish(
            f"cmd/{self._mqtt_topic}", self._mqtt_on_payload
        )
        self.set_state(True)

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the entity on."""
        await self.mqtt_client.async_publish(
            f"cmd/{self._mqtt_topic}", self._mqtt_off_payload
        )
        self.set_state(False)
