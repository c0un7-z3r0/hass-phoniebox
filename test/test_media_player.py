"""Tests for the Phoniebox Media Player."""
from homeassistant.components.media_player.const import REPEAT_MODE_OFF, REPEAT_MODE_ONE
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


async def test_player_volume(hass, mqtt_client_mock, mqtt_mock, mock_phoniebox, config):
    # Initial State
    phoniebox_state = hass.states.get("media_player.phoniebox_test_box")
    assert phoniebox_state.attributes.get("volume_level") == 0.0

    # Various volume changes
    async_fire_mqtt_message(hass, "test_phoniebox/attribute/volume", "5")
    await hass.async_block_till_done()
    phoniebox_state = hass.states.get("media_player.phoniebox_test_box")
    assert phoniebox_state.attributes.get("volume_level") == 0.05

    async_fire_mqtt_message(hass, "test_phoniebox/attribute/volume", "50")
    await hass.async_block_till_done()
    phoniebox_state = hass.states.get("media_player.phoniebox_test_box")
    assert phoniebox_state.attributes.get("volume_level") == 0.5

    async_fire_mqtt_message(hass, "test_phoniebox/attribute/volume", "100")
    await hass.async_block_till_done()
    phoniebox_state = hass.states.get("media_player.phoniebox_test_box")
    assert phoniebox_state.attributes.get("volume_level") == 1.0

    async_fire_mqtt_message(hass, "test_phoniebox/attribute/volume", "0")
    await hass.async_block_till_done()
    phoniebox_state = hass.states.get("media_player.phoniebox_test_box")
    assert phoniebox_state.attributes.get("volume_level") == 0.0

    async_fire_mqtt_message(hass, "test_phoniebox/attribute/volume", "15")
    await hass.async_block_till_done()
    phoniebox_state = hass.states.get("media_player.phoniebox_test_box")
    assert phoniebox_state.attributes.get("volume_level") == 0.15

    async_fire_mqtt_message(hass, "test_phoniebox/attribute/volume", "1.5")
    await hass.async_block_till_done()
    phoniebox_state = hass.states.get("media_player.phoniebox_test_box")
    assert phoniebox_state.attributes.get("volume_level") == 0.015

    async_fire_mqtt_message(hass, "test_phoniebox/attribute/volume", ".5")
    await hass.async_block_till_done()
    phoniebox_state = hass.states.get("media_player.phoniebox_test_box")
    assert phoniebox_state.attributes.get("volume_level") == 0.005


async def test_player_mute(hass, mqtt_client_mock, mqtt_mock, mock_phoniebox, config):
    # Initial State
    phoniebox_state = hass.states.get("media_player.phoniebox_test_box")
    assert phoniebox_state.attributes.get("is_volume_muted") is False

    # Mute the box
    async_fire_mqtt_message(hass, "test_phoniebox/attribute/mute", "true")
    await hass.async_block_till_done()
    phoniebox_state = hass.states.get("media_player.phoniebox_test_box")
    assert phoniebox_state.attributes.get("is_volume_muted") is True

    # Unmute
    async_fire_mqtt_message(hass, "test_phoniebox/attribute/mute", "false")
    await hass.async_block_till_done()
    phoniebox_state = hass.states.get("media_player.phoniebox_test_box")
    assert phoniebox_state.attributes.get("is_volume_muted") is False


async def test_shuffle(hass, mqtt_client_mock, mqtt_mock, mock_phoniebox, config):
    # Initial State
    phoniebox_state = hass.states.get("media_player.phoniebox_test_box")
    assert phoniebox_state.attributes.get("shuffle") is False

    async_fire_mqtt_message(hass, "test_phoniebox/attribute/random", "true")
    await hass.async_block_till_done()
    phoniebox_state = hass.states.get("media_player.phoniebox_test_box")
    assert phoniebox_state.attributes.get("shuffle") is True

    async_fire_mqtt_message(hass, "test_phoniebox/attribute/random", "false")
    await hass.async_block_till_done()
    phoniebox_state = hass.states.get("media_player.phoniebox_test_box")
    assert phoniebox_state.attributes.get("shuffle") is False


async def test_duration(hass, mqtt_client_mock, mqtt_mock, mock_phoniebox, config):
    # Initial State
    phoniebox_state = hass.states.get("media_player.phoniebox_test_box")
    assert phoniebox_state.attributes.get("media_duration") == 0

    async_fire_mqtt_message(hass, "test_phoniebox/attribute/duration", "00:00:55")
    await hass.async_block_till_done()
    phoniebox_state = hass.states.get("media_player.phoniebox_test_box")
    assert phoniebox_state.attributes.get("media_duration") == 55

    async_fire_mqtt_message(hass, "test_phoniebox/attribute/duration", "01:32:55")
    await hass.async_block_till_done()
    phoniebox_state = hass.states.get("media_player.phoniebox_test_box")
    assert phoniebox_state.attributes.get("media_duration") == 5575

    async_fire_mqtt_message(hass, "test_phoniebox/attribute/duration", "00:00:00")
    await hass.async_block_till_done()
    phoniebox_state = hass.states.get("media_player.phoniebox_test_box")
    assert phoniebox_state.attributes.get("media_duration") == 0


async def test_track(hass, mqtt_client_mock, mqtt_mock, mock_phoniebox, config):
    # Initial State
    phoniebox_state = hass.states.get("media_player.phoniebox_test_box")
    assert phoniebox_state.attributes.get("media_track") is None

    async_fire_mqtt_message(hass, "test_phoniebox/attribute/track", "12333")
    await hass.async_block_till_done()
    phoniebox_state = hass.states.get("media_player.phoniebox_test_box")
    assert phoniebox_state.attributes.get("media_track") == 12333

    async_fire_mqtt_message(hass, "test_phoniebox/attribute/track", "0")
    await hass.async_block_till_done()
    phoniebox_state = hass.states.get("media_player.phoniebox_test_box")
    assert phoniebox_state.attributes.get("media_track") == 0


async def test_elapsed(hass, mqtt_client_mock, mqtt_mock, mock_phoniebox, config):
    # Initial State
    phoniebox_state = hass.states.get("media_player.phoniebox_test_box")
    assert phoniebox_state.attributes.get("media_position") == 0

    async_fire_mqtt_message(hass, "test_phoniebox/attribute/elapsed", "00:00:55")
    await hass.async_block_till_done()
    phoniebox_state = hass.states.get("media_player.phoniebox_test_box")
    assert phoniebox_state.attributes.get("media_position") == 55

    async_fire_mqtt_message(hass, "test_phoniebox/attribute/elapsed", "01:32:55")
    await hass.async_block_till_done()
    phoniebox_state = hass.states.get("media_player.phoniebox_test_box")
    assert phoniebox_state.attributes.get("media_position") == 5575

    async_fire_mqtt_message(hass, "test_phoniebox/attribute/elapsed", "00:00:00")
    await hass.async_block_till_done()
    phoniebox_state = hass.states.get("media_player.phoniebox_test_box")
    assert phoniebox_state.attributes.get("media_position") == 0


async def test_artist(hass, mqtt_client_mock, mqtt_mock, mock_phoniebox, config):
    # Initial State
    phoniebox_state = hass.states.get("media_player.phoniebox_test_box")
    assert phoniebox_state.attributes.get("media_artist") is None

    async_fire_mqtt_message(hass, "test_phoniebox/attribute/artist", "Artist")
    await hass.async_block_till_done()
    phoniebox_state = hass.states.get("media_player.phoniebox_test_box")
    assert phoniebox_state.attributes.get("media_artist") == "Artist"

    async_fire_mqtt_message(hass, "test_phoniebox/attribute/artist", "Artist2")
    await hass.async_block_till_done()
    phoniebox_state = hass.states.get("media_player.phoniebox_test_box")
    assert phoniebox_state.attributes.get("media_artist") == "Artist2"


async def test_title(hass, mqtt_client_mock, mqtt_mock, mock_phoniebox, config):
    # Initial State
    phoniebox_state = hass.states.get("media_player.phoniebox_test_box")
    assert phoniebox_state.attributes.get("media_title") is None

    async_fire_mqtt_message(hass, "test_phoniebox/attribute/title", "Awesome Title")
    await hass.async_block_till_done()
    phoniebox_state = hass.states.get("media_player.phoniebox_test_box")
    assert phoniebox_state.attributes.get("media_title") == "Awesome Title"

    async_fire_mqtt_message(hass, "test_phoniebox/attribute/title", "Awesome Title 2")
    await hass.async_block_till_done()
    phoniebox_state = hass.states.get("media_player.phoniebox_test_box")
    assert phoniebox_state.attributes.get("media_title") == "Awesome Title 2"


async def test_album(hass, mqtt_client_mock, mqtt_mock, mock_phoniebox, config):
    # Initial State
    phoniebox_state = hass.states.get("media_player.phoniebox_test_box")
    assert phoniebox_state.attributes.get("media_album_name") is None

    async_fire_mqtt_message(hass, "test_phoniebox/attribute/album", "Awesome album")
    await hass.async_block_till_done()
    phoniebox_state = hass.states.get("media_player.phoniebox_test_box")
    assert phoniebox_state.attributes.get("media_album_name") == "Awesome album"

    async_fire_mqtt_message(hass, "test_phoniebox/attribute/album", "Awesome album 2")
    await hass.async_block_till_done()
    phoniebox_state = hass.states.get("media_player.phoniebox_test_box")
    assert phoniebox_state.attributes.get("media_album_name") == "Awesome album 2"


async def test_repeat(hass, mqtt_client_mock, mqtt_mock, mock_phoniebox, config):
    # Initial State
    phoniebox_state = hass.states.get("media_player.phoniebox_test_box")
    assert phoniebox_state.attributes.get("media_album_name") is None

    async_fire_mqtt_message(hass, "test_phoniebox/attribute/repeat", "true")
    await hass.async_block_till_done()
    phoniebox_state = hass.states.get("media_player.phoniebox_test_box")
    assert phoniebox_state.attributes.get("repeat") == REPEAT_MODE_ONE

    async_fire_mqtt_message(hass, "test_phoniebox/attribute/repeat", "false")
    await hass.async_block_till_done()
    phoniebox_state = hass.states.get("media_player.phoniebox_test_box")
    assert phoniebox_state.attributes.get("repeat") == REPEAT_MODE_OFF
