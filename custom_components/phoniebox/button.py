"""Buttons to control the phoniebox."""

from __future__ import annotations

from abc import ABC
from dataclasses import dataclass
from typing import TYPE_CHECKING, override

from homeassistant.components.button import ButtonDeviceClass, ButtonEntity

from .const import (
    ALL_BUTTONS,
    BUTTON_RESTART,
    CONF_PHONIEBOX_NAME,
    DOMAIN,
    LOGGER,
    NAME_TO_MQTT_COMMAND,
)
from .entity import PhonieboxEntity
from .sensor import _slug

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from . import DataCoordinator


@dataclass
class ButtonData:
    """Button Data."""

    name: str
    device_class: ButtonDeviceClass | None = None
    on_press_mqtt_topic: str | None = None


def find_device_class(name: str) -> ButtonDeviceClass | None:
    """Based on the button name find the corresponding device class."""
    if name == BUTTON_RESTART:
        return ButtonDeviceClass.RESTART
    return None


def find_mqtt_topic(name: str) -> str | None:
    """Based on the button name find the corresponding mqtt command."""
    return getattr(NAME_TO_MQTT_COMMAND, name, None)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_devices: AddEntitiesCallback
) -> None:
    """Set button platform up."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    buttons: list[PhonieboxButton] = []
    store = coordinator.buttons

    buttons.extend(
        PhonieboxButton(
            config_entry=entry,
            coordinator=coordinator,
            data=ButtonData(
                name=button_name,
                device_class=find_device_class(button_name),
                on_press_mqtt_topic=find_mqtt_topic(button_name),
            ),
        )
        for button_name in ALL_BUTTONS
    )

    if len(buttons) == 0:
        return

    for button in buttons:
        if button.name not in store:
            button.hass = hass
            store[button.name] = button
            LOGGER.debug(
                "Registering buttons %(name)s",
                {"name": button.name},
            )
            async_add_devices(new_entities=(button,), update_before_add=True)


class PhonieboxButton(PhonieboxEntity, ButtonEntity, ABC):
    """phoniebox button class."""

    _attr_should_poll = False

    def __init__(
        self,
        config_entry: ConfigEntry,
        coordinator: DataCoordinator,
        data: ButtonData,
    ) -> None:
        """Init the button."""
        super().__init__(config_entry, coordinator)
        self.entity_id = _slug(data.name, config_entry.data[CONF_PHONIEBOX_NAME])
        self._attr_name = data.name
        self._attr_device_class = data.device_class
        self._on_press_mqtt_topic = data.on_press_mqtt_topic

    @override
    async def async_press(self) -> None:
        """Press the button."""
        if self._on_press_mqtt_topic is not None:
            LOGGER.info(
                "Pressing button ------> %(topic)s",
                {"topic": self._on_press_mqtt_topic},
            )
            await self.mqtt_client.async_publish(
                f"cmd/{self._on_press_mqtt_topic}", None
            )
