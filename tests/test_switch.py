"""Tests for the Phoniebox Binary Sensors."""

from typing import TYPE_CHECKING
from unittest.mock import MagicMock

from homeassistant.const import (
    ATTR_ENTITY_ID,
    SERVICE_TURN_OFF,
    SERVICE_TURN_ON,
    STATE_OFF,
    STATE_ON,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er
from pytest_homeassistant_custom_component.common import (
    MockConfigEntry,
    async_fire_mqtt_message,
)

from tests.typing import MqttMockHAClient

if TYPE_CHECKING:
    from homeassistant.helpers.entity_registry import RegistryEntry


async def test_switch_registry(
    hass: HomeAssistant,
    mock_phoniebox: MockConfigEntry,
    config: dict,
) -> None:
    """Test that a new sensor is created."""
    entity_registry = er.async_get(hass)
    er_items_before = er.async_entries_for_config_entry(
        entity_registry, mock_phoniebox.entry_id
    )

    async_fire_mqtt_message(hass, "test_phoniebox/attribute/gpio", "true")
    await hass.async_block_till_done()

    er_items_after = er.async_entries_for_config_entry(
        entity_registry, mock_phoniebox.entry_id
    )
    assert (
        len(er_items_after) == len(er_items_before) + 2
    )  # now added the sensor and for binary most-likely a switch as well

    entry: RegistryEntry = entity_registry.async_get("switch.phoniebox_test_box_gpio")
    assert entry
    assert entry.unique_id == "test_box-switch.phoniebox_test_box_gpio"

    switch_state = hass.states.get("switch.phoniebox_test_box_gpio")
    assert switch_state is not None
    assert switch_state.state == STATE_ON


async def test_switch_registry_update(
    hass: HomeAssistant,
    mock_phoniebox: MockConfigEntry,
    config: dict,
) -> None:
    """Test that the sensor is updating properly on new value."""
    async_fire_mqtt_message(hass, "test_phoniebox/attribute/gpio", "true")
    await hass.async_block_till_done()
    async_fire_mqtt_message(hass, "test_phoniebox/attribute/gpio", "false")
    await hass.async_block_till_done()

    switch_state = hass.states.get("switch.phoniebox_test_box_gpio")
    assert switch_state is not None
    assert switch_state.state == STATE_OFF


async def test_switch_off(
    hass: HomeAssistant,
    mqtt_mock: MqttMockHAClient,
    mock_phoniebox: MockConfigEntry,
    config: dict,
) -> None:
    """Test that the sensor is updating properly on new value."""
    async_fire_mqtt_message(hass, "test_phoniebox/attribute/gpio", "true")
    await hass.async_block_till_done()

    switch_state = hass.states.get("switch.phoniebox_test_box_gpio")
    assert switch_state is not None
    assert switch_state.state == STATE_ON

    data = {ATTR_ENTITY_ID: switch_state.entity_id}
    await hass.services.async_call("switch", SERVICE_TURN_OFF, data, blocking=True)
    mqtt_mock.async_publish.assert_called_once_with(
        "test_phoniebox/cmd/gpio", "stop", 0, False
    )
    switch_state = hass.states.get("switch.phoniebox_test_box_gpio")
    assert switch_state is not None
    assert switch_state.state == STATE_OFF


async def test_switch_on(
    hass: HomeAssistant,
    mqtt_mock: MagicMock,
    mock_phoniebox: MockConfigEntry,
    config: dict,
) -> None:
    """Test that the sensor is updating properly on new value."""
    async_fire_mqtt_message(hass, "test_phoniebox/attribute/gpio", "false")
    await hass.async_block_till_done()

    switch_state = hass.states.get("switch.phoniebox_test_box_gpio")
    assert switch_state is not None
    assert switch_state.state == STATE_OFF

    data = {ATTR_ENTITY_ID: switch_state.entity_id}
    await hass.services.async_call("switch", SERVICE_TURN_ON, data, blocking=True)
    mqtt_mock.async_publish.assert_called_once_with(
        "test_phoniebox/cmd/gpio", "start", 0, False
    )
    switch_state = hass.states.get(switch_state.entity_id)
    assert switch_state is not None
    assert switch_state.state == STATE_ON
