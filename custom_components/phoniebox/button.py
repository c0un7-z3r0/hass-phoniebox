"""Buttons for phoniebox."""
from __future__ import annotations

import logging
from abc import ABC

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.components.button import ButtonEntity, ButtonDeviceClass
from homeassistant.config_entries import ConfigEntries

from . import DataCoordinator
from .const import BOOLEAN_SENSORS, CONF_PHONIEBOX_NAME, DOMAIN, NAME, VERSION, BUTTONS
from .entity import PhonieboxEntity
from .sensor import _slug
from .utils import string_to_bool

_LOGGER: logging.Logger = logging.getLogger(__package__)


def find_device_class(domain: str) -> BinarySensorDeviceClass | None:
    """
    Based on the domain find the corresponding device class
    """
    return None


def find_mqtt_topic(domain: str) -> str | None:
    if domain == "random":
        return "playershuffle"

    return None


def discover_buttons(topic, entry, coordinator):
    """
    Based on the topic and entry create the correct binary sensor
    """
    parts = topic.split("/")
    domain = parts[2] if len(parts) == 3 else parts[1]

    if domain not in BUTTONS:
        return

    return PhonieboxButton(
        config_entry=entry,
        name=domain,
        coordinator=coordinator,
        device_class=find_device_class(domain),
        on_press_mqtt_topic=find_mqtt_topic(domain),
    )


async def async_setup_entry(hass, entry, async_add_devices):
    """Setup button platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    def received_msg(msg):
        buttons = discover_buttons(msg.topic, entry, coordinator)
        store = coordinator.buttons

        if not buttons:
            return

        if isinstance(buttons, PhonieboxButton):
            buttons = (buttons,)

        for button in buttons:
            if button.name not in store:
                button.hass = hass
                store[button.name] = button
                _LOGGER.debug(
                    "Registering buttons %(name)s",
                    {"name": button.name},
                )
                async_add_devices((button,), True)

    await coordinator.mqtt_client.async_subscribe("#", received_msg)


class PhonieboxButton(PhonieboxEntity, ButtonEntity, ABC):
    """phoniebox button class."""

    _attr_should_poll = False

    def __init__(
            self,
            config_entry: ConfigEntries,
            name: str,
            coordinator: DataCoordinator,
            device_class: ButtonDeviceClass = None,
            on_press_mqtt_topic=None,
    ):
        super().__init__(config_entry, coordinator)
        self.entity_id = _slug(name, config_entry.data[CONF_PHONIEBOX_NAME])
        self._attr_name = name
        self._attr_device_class = device_class
        self._on_press_mqtt_topic = on_press_mqtt_topic

    async def async_press(self) -> None:
        """Press the button."""
        if self._on_press_mqtt_topic:
            await self.mqtt_client.async_publish(
                "cmd/" + self._on_press_mqtt_topic, {}
            )
