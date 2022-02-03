"""Buttons to control the phoniebox."""
from __future__ import annotations

import logging
from abc import ABC

from homeassistant.components.button import ButtonEntity, ButtonDeviceClass
from homeassistant.config_entries import ConfigEntries

from . import DataCoordinator
from .const import CONF_PHONIEBOX_NAME, DOMAIN, PHONIEBOX_CMD_PLAYER_SHUFFLE, \
    PHONIEBOX_CMD_SCAN, PHONIEBOX_CMD_PLAYER_REWIND, PHONIEBOX_CMD_PLAYER_REPLAY, PHONIEBOX_CMD_REBOOT, \
    PHONIEBOX_CMD_SHUTDOWN, PHONIEBOX_CMD_SHUTDOWN_SILENT, BUTTON_RESTART, BUTTON_SHUFFLE, BUTTON_SCAN, BUTTON_REWIND, \
    BUTTON_REPLAY, BUTTON_SHUTDOWN, BUTTON_SHUTDOWN_SILENT, ALL_BUTTONS
from .entity import PhonieboxEntity
from .sensor import _slug

_LOGGER: logging.Logger = logging.getLogger(__package__)


def find_device_class(name: str) -> ButtonDeviceClass | None:
    """
    Based on the button name find the corresponding device class
    """
    if name == BUTTON_RESTART:
        return ButtonDeviceClass.RESTART
    return None


def find_mqtt_topic(name: str) -> str:
    """
    Based on the button name find the corresponding mqtt command
    """
    if name == BUTTON_SHUFFLE:
        return PHONIEBOX_CMD_PLAYER_SHUFFLE
    if name == BUTTON_SCAN:
        return PHONIEBOX_CMD_SCAN
    if name == BUTTON_REWIND:
        return PHONIEBOX_CMD_PLAYER_REWIND
    if name == BUTTON_REPLAY:
        return PHONIEBOX_CMD_PLAYER_REPLAY
    if name == BUTTON_RESTART:
        return PHONIEBOX_CMD_REBOOT
    if name == BUTTON_SHUTDOWN:
        return PHONIEBOX_CMD_SHUTDOWN
    if name == BUTTON_SHUTDOWN_SILENT:
        return PHONIEBOX_CMD_SHUTDOWN_SILENT


async def async_setup_entry(hass, entry, async_add_devices):
    """Setup button platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    buttons: list[PhonieboxButton] = []
    store = coordinator.buttons

    for button_name in ALL_BUTTONS:
        buttons.append(
            PhonieboxButton(
                config_entry=entry,
                name=button_name,
                coordinator=coordinator,
                device_class=find_device_class(button_name),
                on_press_mqtt_topic=find_mqtt_topic(button_name),
            )
        )

    if len(buttons) == 0:
        return

    for button in buttons:
        if button.name not in store:
            button.hass = hass
            store[button.name] = button
            _LOGGER.debug(
                "Registering buttons %(name)s",
                {"name": button.name},
            )
            async_add_devices((button,), True)


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
