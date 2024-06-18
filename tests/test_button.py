"""Tests for the Phoniebox Buttons."""

from typing import TYPE_CHECKING

from homeassistant.components.button import SERVICE_PRESS
from homeassistant.const import ATTR_ENTITY_ID
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.phoniebox.button import find_mqtt_topic
from custom_components.phoniebox.const import ALL_BUTTONS
from tests.typing import MqttMockHAClient

if TYPE_CHECKING:
    from homeassistant.helpers.entity_registry import RegistryEntry


async def test_button_registry(
    hass: HomeAssistant,
    mock_phoniebox: MockConfigEntry,
    config: dict,
) -> None:
    """Test that all the buttons are registered."""
    entity_registry = er.async_get(hass)
    er_items: list[RegistryEntry] = er.async_entries_for_config_entry(
        entity_registry, mock_phoniebox.entry_id
    )
    registered_buttons = list(filter(lambda item: item.domain == "button", er_items))
    assert len(registered_buttons) == len(ALL_BUTTONS)


async def test_button_press(
    hass: HomeAssistant,
    mqtt_mock: MqttMockHAClient,
    mock_phoniebox: MockConfigEntry,
    config: dict,
) -> None:
    """Verify button press triggers mqtt cmd."""
    entity_registry = er.async_get(hass)
    er_items: list[RegistryEntry] = er.async_entries_for_config_entry(
        entity_registry, mock_phoniebox.entry_id
    )
    registered_buttons = list(filter(lambda item: item.domain == "button", er_items))

    test_button: RegistryEntry = registered_buttons[0]
    data = {ATTR_ENTITY_ID: test_button.entity_id}
    await hass.services.async_call("button", SERVICE_PRESS, data, blocking=True)

    assert test_button.original_name is not None
    button_mqtt_topic = find_mqtt_topic(test_button.original_name)
    assert button_mqtt_topic is not None
    await hass.async_block_till_done()

    # test_phoniebox/cmd/scan
    mqtt_mock.async_publish.assert_called_once_with(
        "test_phoniebox/cmd/" + button_mqtt_topic, None, 0, False
    )
