"""Tests for the Phoniebox Buttons."""
from homeassistant.components.button import SERVICE_PRESS
from homeassistant.const import ATTR_ENTITY_ID
from homeassistant.core import State, HomeAssistant
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.entity_registry import RegistryEntry

from custom_components.phoniebox.button import find_mqtt_topic
from custom_components.phoniebox.const import ALL_BUTTONS


async def test_button_registry(
        hass: HomeAssistant, mqtt_client_mock, mqtt_mock, mock_phoniebox, config
):
    """Test that all the buttons are registered"""
    entity_registry = er.async_get(hass)
    er_items: list[RegistryEntry] = er.async_entries_for_config_entry(
        entity_registry, mock_phoniebox.entry_id
    )
    registered_buttons = list(filter(lambda item: item.domain == "button", er_items))
    assert len(registered_buttons) == len(ALL_BUTTONS)


async def test_button_press(
        hass: HomeAssistant, mqtt_client_mock, mqtt_mock, mock_phoniebox, config
):
    entity_registry = er.async_get(hass)
    er_items: list[RegistryEntry] = er.async_entries_for_config_entry(
        entity_registry, mock_phoniebox.entry_id
    )
    registered_buttons = list(filter(lambda item: item.domain == "button", er_items))

    test_button = registered_buttons[0]
    data = {ATTR_ENTITY_ID: test_button.entity_id}
    await hass.services.async_call("button", SERVICE_PRESS, data, blocking=True)

    button_mqtt_topic = find_mqtt_topic(test_button.original_name)
    assert button_mqtt_topic is not None

    mqtt_mock.async_publish.assert_called_once_with(
        "test_phoniebox/cmd/" + button_mqtt_topic, "{}", 0, False
    )
