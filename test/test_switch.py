"""Tests for the Phoniebox Binary Sensors."""
from homeassistant.const import STATE_ON, STATE_OFF, ATTR_ENTITY_ID, SERVICE_TURN_OFF, SERVICE_TURN_ON
from homeassistant.core import State
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.entity_registry import RegistryEntry
from pytest_homeassistant_custom_component import common
from pytest_homeassistant_custom_component.common import async_fire_mqtt_message

from custom_components.phoniebox import DOMAIN


async def test_switch_registry(hass, mqtt_client_mock, mqtt_mock, mock_phoniebox, config):
    """ Test that a new sensor is created """
    entity_registry = er.async_get(hass)
    er_items_before = er.async_entries_for_config_entry(entity_registry, mock_phoniebox.entry_id)

    async_fire_mqtt_message(hass, "test_phoniebox/attribute/gpio", "true")
    await hass.async_block_till_done()

    er_items_after = er.async_entries_for_config_entry(entity_registry, mock_phoniebox.entry_id)
    assert len(er_items_after) == len(
        er_items_before) + 2  # now added the sensor and for binary most-likely a switch as well

    entry: RegistryEntry = entity_registry.async_get("switch.phoniebox_test_box_gpio_2")
    assert entry
    assert entry.unique_id == 'test_boxswitch.phoniebox_test_box_gpio'

    switch_state = hass.states.get("switch.phoniebox_test_box_gpio_2")
    assert switch_state is not None
    assert switch_state.state == STATE_ON


async def test_switch_registry_update(hass, mqtt_client_mock, mqtt_mock, mock_phoniebox, config):
    """ Test that the sensor is updating properly on new value """
    async_fire_mqtt_message(hass, "test_phoniebox/attribute/gpio", "true")
    await hass.async_block_till_done()
    async_fire_mqtt_message(hass, "test_phoniebox/attribute/gpio", "false")
    await hass.async_block_till_done()

    switch_state = hass.states.get("switch.phoniebox_test_box_gpio_2")
    assert switch_state is not None
    assert switch_state.state == STATE_OFF


async def test_switch_off(hass, mqtt_client_mock, mqtt_mock, mock_phoniebox, config):
    """ Test that the sensor is updating properly on new value """
    async_fire_mqtt_message(hass, "test_phoniebox/attribute/gpio", "true")
    await hass.async_block_till_done()

    switch_state: State = hass.states.get("switch.phoniebox_test_box_gpio_2")
    assert switch_state is not None
    assert switch_state.state == STATE_ON

    data = {ATTR_ENTITY_ID: switch_state.entity_id}
    await hass.services.async_call("switch", SERVICE_TURN_OFF, data, blocking=True)
    mqtt_mock.async_publish.assert_called_once_with(
        "test_phoniebox/cmd/gpio", 'stop', 0, False
    )

    assert hass.states.get(switch_state.entity_id).state == STATE_OFF


async def test_switch_on(hass, mqtt_client_mock, mqtt_mock, mock_phoniebox, config):
    """ Test that the sensor is updating properly on new value """
    async_fire_mqtt_message(hass, "test_phoniebox/attribute/random", "false")
    await hass.async_block_till_done()

    switch_state: State = hass.states.get("switch.phoniebox_test_box_random_2")
    assert switch_state is not None
    assert switch_state.state == STATE_OFF

    data = {ATTR_ENTITY_ID: switch_state.entity_id}
    await hass.services.async_call("switch", SERVICE_TURN_ON, data, blocking=True)
    mqtt_mock.async_publish.assert_called_once_with(
        "test_phoniebox/cmd/playershuffle", '', 0, False
    )

    assert hass.states.get(switch_state.entity_id).state == STATE_ON
