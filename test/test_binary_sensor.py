"""Tests for the Phoniebox Binary Sensors."""
from homeassistant.const import STATE_OFF, STATE_ON
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.entity_registry import RegistryEntry
from pytest_homeassistant_custom_component.common import async_fire_mqtt_message


async def test_sensor_registry(
    hass, mqtt_client_mock, mqtt_mock, mock_phoniebox, config
):
    """Test that a new sensor is created"""
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

    entry: RegistryEntry = entity_registry.async_get(
        "binary_sensor.phoniebox_test_box_gpio"
    )
    assert entry
    assert entry.unique_id == "test_box-binary_sensor.phoniebox_test_box_gpio"

    version_sensor_state = hass.states.get("binary_sensor.phoniebox_test_box_gpio")
    assert version_sensor_state is not None
    assert version_sensor_state.state == STATE_ON


async def test_sensor_registry_update(
    hass, mqtt_client_mock, mqtt_mock, mock_phoniebox, config
):
    """Test that the sensor is updating properly on new value"""
    async_fire_mqtt_message(hass, "test_phoniebox/attribute/gpio", "true")
    await hass.async_block_till_done()
    async_fire_mqtt_message(hass, "test_phoniebox/attribute/gpio", "false")
    await hass.async_block_till_done()

    version_sensor_state = hass.states.get("binary_sensor.phoniebox_test_box_gpio")
    assert version_sensor_state is not None
    assert version_sensor_state.state == STATE_OFF
