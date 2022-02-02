"""Tests for the Phoniebox Media Player."""

from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.entity_registry import RegistryEntry
from pytest_homeassistant_custom_component.common import async_fire_mqtt_message

from custom_components.phoniebox.const import SUPPORT_MQTTMEDIAPLAYER


async def test_device_registry(hass, mqtt_client_mock, mqtt_mock, mock_phoniebox, config):
    entity_registry = er.async_get(hass)
    entry: RegistryEntry = entity_registry.async_get("media_player.phoniebox_test_box")
    assert entry
    assert entry.unique_id == "test_box"
    assert entry.domain == "media_player"
    assert entry.platform == "phoniebox"
    assert entry.disabled is False

    phoniebox_state = hass.states.get("media_player.phoniebox_test_box")
    assert phoniebox_state is not None
    assert phoniebox_state.state == "idle"
    assert phoniebox_state.attributes.get("shuffle") is False
    assert phoniebox_state.attributes.get("volume_level") == 0.0
    assert phoniebox_state.attributes.get("supported_features") == SUPPORT_MQTTMEDIAPLAYER


async def test_player_states(hass, mqtt_client_mock, mqtt_mock, mock_phoniebox, config):
    # Initial State
    phoniebox_state = hass.states.get("media_player.phoniebox_test_box")
    assert phoniebox_state.state == "idle"

    # Playing State
    async_fire_mqtt_message(hass, "test_phoniebox/attribute/state", "play")
    await hass.async_block_till_done()
    phoniebox_state = hass.states.get("media_player.phoniebox_test_box")
    assert phoniebox_state.state == "playing"

    # Paused State
    async_fire_mqtt_message(hass, "test_phoniebox/attribute/state", "pause")
    await hass.async_block_till_done()
    phoniebox_state = hass.states.get("media_player.phoniebox_test_box")
    assert phoniebox_state.state == "paused"

    # Stopped State
    async_fire_mqtt_message(hass, "test_phoniebox/attribute/state", "stop")
    await hass.async_block_till_done()
    phoniebox_state = hass.states.get("media_player.phoniebox_test_box")
    assert phoniebox_state.state == "idle"
