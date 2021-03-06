"""Tests for the Phoniebox Media Player."""
import pytest
from homeassistant.components.media_player.const import (
    ATTR_MEDIA_REPEAT,
    ATTR_MEDIA_SEEK_POSITION,
    ATTR_MEDIA_SHUFFLE,
    ATTR_MEDIA_VOLUME_LEVEL,
    ATTR_MEDIA_VOLUME_MUTED,
    REPEAT_MODE_ALL,
    REPEAT_MODE_OFF,
    REPEAT_MODE_ONE, ATTR_MEDIA_DURATION, ATTR_MEDIA_TRACK, ATTR_MEDIA_POSITION, ATTR_MEDIA_ARTIST, ATTR_MEDIA_TITLE,
    ATTR_MEDIA_ALBUM_NAME,
)
from homeassistant.const import (
    ATTR_ENTITY_ID,
    SERVICE_MEDIA_NEXT_TRACK,
    SERVICE_MEDIA_PAUSE,
    SERVICE_MEDIA_PLAY,
    SERVICE_MEDIA_PREVIOUS_TRACK,
    SERVICE_MEDIA_SEEK,
    SERVICE_MEDIA_STOP,
    SERVICE_REPEAT_SET,
    SERVICE_SHUFFLE_SET,
    SERVICE_TURN_OFF,
    SERVICE_VOLUME_DOWN,
    SERVICE_VOLUME_MUTE,
    SERVICE_VOLUME_SET,
    SERVICE_VOLUME_UP, STATE_UNAVAILABLE, STATE_PLAYING, STATE_PAUSED, STATE_IDLE, STATE_OFF,
)

from pytest_homeassistant_custom_component.common import async_fire_mqtt_message

from custom_components.phoniebox.const import (
    PHONIEBOX_REPEAT_OFF,
    PHONIEBOX_REPEAT_PLAYLIST,
    PHONIEBOX_REPEAT_SINGLE,
    SUPPORT_MQTTMEDIAPLAYER,
)


async def test_device_registry(
        hass, mqtt_client_mock, mqtt_mock, mock_phoniebox, config, media_player_entry
):
    assert media_player_entry
    assert media_player_entry.unique_id == "test_box-media_player.phoniebox_test_box"
    assert media_player_entry.domain == "media_player"
    assert media_player_entry.platform == "phoniebox"
    assert media_player_entry.disabled is False

    phoniebox_state = hass.states.get("media_player.phoniebox_test_box")
    assert phoniebox_state is not None
    assert phoniebox_state.state == STATE_UNAVAILABLE
    assert phoniebox_state.attributes.get(ATTR_MEDIA_SHUFFLE) is False
    assert phoniebox_state.attributes.get(ATTR_MEDIA_VOLUME_LEVEL) == 0.0
    assert (
            phoniebox_state.attributes.get("supported_features") == SUPPORT_MQTTMEDIAPLAYER
    )


async def test_device_state(
        hass, mqtt_client_mock, mqtt_mock, mock_phoniebox, config, media_player_entry
):
    phoniebox_state = hass.states.get("media_player.phoniebox_test_box")
    assert phoniebox_state.state == STATE_UNAVAILABLE

    async_fire_mqtt_message(hass, "test_phoniebox/state", "online")
    await hass.async_block_till_done()
    phoniebox_state = hass.states.get("media_player.phoniebox_test_box")
    assert phoniebox_state.state == STATE_IDLE

    async_fire_mqtt_message(hass, "test_phoniebox/state", "offline")
    await hass.async_block_till_done()
    phoniebox_state = hass.states.get("media_player.phoniebox_test_box")
    assert phoniebox_state.state == STATE_OFF

    async_fire_mqtt_message(hass, "test_phoniebox/state", "online")
    await hass.async_block_till_done()
    phoniebox_state = hass.states.get("media_player.phoniebox_test_box")
    assert phoniebox_state.state == STATE_IDLE

    async_fire_mqtt_message(hass, "test_phoniebox/attribute/state", "pause")
    await hass.async_block_till_done()
    phoniebox_state = hass.states.get("media_player.phoniebox_test_box")
    assert phoniebox_state.state == STATE_PAUSED


async def test_off_device_state_change_to_paused(
        hass, mqtt_client_mock, mqtt_mock, mock_phoniebox, config, media_player_entry
):
    async_fire_mqtt_message(hass, "test_phoniebox/state", "offline")
    await hass.async_block_till_done()
    phoniebox_state = hass.states.get("media_player.phoniebox_test_box")
    assert phoniebox_state.state == STATE_OFF

    # now the box is "off" and should change to paused
    async_fire_mqtt_message(hass, "test_phoniebox/attribute/state", "pause")
    await hass.async_block_till_done()
    phoniebox_state = hass.states.get("media_player.phoniebox_test_box")
    assert phoniebox_state.state == STATE_PAUSED


async def test_off_device_state_change_to_online(
        hass, mqtt_client_mock, mqtt_mock, mock_phoniebox, config, media_player_entry
):
    async_fire_mqtt_message(hass, "test_phoniebox/state", "offline")
    await hass.async_block_till_done()
    phoniebox_state = hass.states.get("media_player.phoniebox_test_box")
    assert phoniebox_state.state == STATE_OFF

    # now the box is "off" and should change to idle
    async_fire_mqtt_message(hass, "test_phoniebox/state", "online")
    await hass.async_block_till_done()
    phoniebox_state = hass.states.get("media_player.phoniebox_test_box")
    assert phoniebox_state.state == STATE_IDLE


async def test_unvailable_device_state_change_to_online(
        hass, mqtt_client_mock, mqtt_mock, mock_phoniebox, config, media_player_entry
):
    async_fire_mqtt_message(hass, "test_phoniebox/state", "online")
    await hass.async_block_till_done()
    phoniebox_state = hass.states.get("media_player.phoniebox_test_box")
    assert phoniebox_state.state == STATE_IDLE


async def test_online_device_state_change_to_online(
        hass, mqtt_client_mock, mqtt_mock, mock_phoniebox, config, media_player_entry
):
    async_fire_mqtt_message(hass, "test_phoniebox/attribute/state", "play")
    await hass.async_block_till_done()
    phoniebox_state = hass.states.get("media_player.phoniebox_test_box")
    assert phoniebox_state.state == STATE_PLAYING

    # should not change
    async_fire_mqtt_message(hass, "test_phoniebox/state", "online")
    await hass.async_block_till_done()
    phoniebox_state = hass.states.get("media_player.phoniebox_test_box")
    assert phoniebox_state.state == STATE_PLAYING


async def test_cmd_volume_up(
        hass, mqtt_client_mock, mqtt_mock, mock_phoniebox, config, media_player_entry
):
    data = {ATTR_ENTITY_ID: media_player_entry.entity_id}
    await hass.services.async_call(
        "media_player", SERVICE_VOLUME_UP, data, blocking=True
    )
    mqtt_mock.async_publish.assert_called_once_with(
        "test_phoniebox/cmd/volumeup", "{}", 0, False
    )


async def test_cmd_volume_down(
        hass, mqtt_client_mock, mqtt_mock, mock_phoniebox, config, media_player_entry
):
    data = {ATTR_ENTITY_ID: media_player_entry.entity_id}
    await hass.services.async_call(
        "media_player", SERVICE_VOLUME_DOWN, data, blocking=True
    )
    mqtt_mock.async_publish.assert_called_once_with(
        "test_phoniebox/cmd/volumedown", "{}", 0, False
    )


async def test_cmd_mute(
        hass, mqtt_client_mock, mqtt_mock, mock_phoniebox, config, media_player_entry
):
    data = {ATTR_ENTITY_ID: media_player_entry.entity_id, ATTR_MEDIA_VOLUME_MUTED: True}
    await hass.services.async_call(
        "media_player", SERVICE_VOLUME_MUTE, data, blocking=True
    )
    mqtt_mock.async_publish.assert_called_once_with(
        "test_phoniebox/cmd/mute", "true", 0, False
    )


async def test_cmd_unmute(
        hass, mqtt_client_mock, mqtt_mock, mock_phoniebox, config, media_player_entry
):
    data = {
        ATTR_ENTITY_ID: media_player_entry.entity_id,
        ATTR_MEDIA_VOLUME_MUTED: False,
    }
    await hass.services.async_call(
        "media_player", SERVICE_VOLUME_MUTE, data, blocking=True
    )
    mqtt_mock.async_publish.assert_called_once_with(
        "test_phoniebox/cmd/mute", "false", 0, False
    )


async def test_cmd_play(
        hass, mqtt_client_mock, mqtt_mock, mock_phoniebox, config, media_player_entry
):
    data = {ATTR_ENTITY_ID: media_player_entry.entity_id}
    await hass.services.async_call(
        "media_player", SERVICE_MEDIA_PLAY, data, blocking=True
    )
    mqtt_mock.async_publish.assert_called_once_with(
        "test_phoniebox/cmd/playerplay", "{}", 0, False
    )


async def test_cmd_pause(
        hass, mqtt_client_mock, mqtt_mock, mock_phoniebox, config, media_player_entry
):
    data = {ATTR_ENTITY_ID: media_player_entry.entity_id}
    await hass.services.async_call(
        "media_player", SERVICE_MEDIA_PAUSE, data, blocking=True
    )
    mqtt_mock.async_publish.assert_called_once_with(
        "test_phoniebox/cmd/playerpause", "{}", 0, False
    )


async def test_cmd_stop(
        hass, mqtt_client_mock, mqtt_mock, mock_phoniebox, config, media_player_entry
):
    data = {ATTR_ENTITY_ID: media_player_entry.entity_id}
    await hass.services.async_call(
        "media_player", SERVICE_MEDIA_STOP, data, blocking=True
    )
    mqtt_mock.async_publish.assert_called_once_with(
        "test_phoniebox/cmd/playerstop", "{}", 0, False
    )


async def test_cmd_play_prev(
        hass, mqtt_client_mock, mqtt_mock, mock_phoniebox, config, media_player_entry
):
    data = {ATTR_ENTITY_ID: media_player_entry.entity_id}
    await hass.services.async_call(
        "media_player", SERVICE_MEDIA_PREVIOUS_TRACK, data, blocking=True
    )
    mqtt_mock.async_publish.assert_called_once_with(
        "test_phoniebox/cmd/playerprev", "{}", 0, False
    )


async def test_cmd_play_next(
        hass, mqtt_client_mock, mqtt_mock, mock_phoniebox, config, media_player_entry
):
    data = {ATTR_ENTITY_ID: media_player_entry.entity_id}
    await hass.services.async_call(
        "media_player", SERVICE_MEDIA_NEXT_TRACK, data, blocking=True
    )
    mqtt_mock.async_publish.assert_called_once_with(
        "test_phoniebox/cmd/playernext", "{}", 0, False
    )


async def test_cmd_seek(
        hass, mqtt_client_mock, mqtt_mock, mock_phoniebox, config, media_player_entry
):
    data = {
        ATTR_ENTITY_ID: media_player_entry.entity_id,
        ATTR_MEDIA_SEEK_POSITION: 10.0,
    }
    await hass.services.async_call(
        "media_player", SERVICE_MEDIA_SEEK, data, blocking=True
    )
    mqtt_mock.async_publish.assert_called_once_with(
        "test_phoniebox/cmd/playerseek", "10.0", 0, False
    )


async def test_cmd_shuffle_true(
        hass, mqtt_client_mock, mqtt_mock, mock_phoniebox, config, media_player_entry
):
    data = {ATTR_ENTITY_ID: media_player_entry.entity_id, ATTR_MEDIA_SHUFFLE: "true"}
    await hass.services.async_call(
        "media_player", SERVICE_SHUFFLE_SET, data, blocking=True
    )
    mqtt_mock.async_publish.assert_called_once_with(
        "test_phoniebox/cmd/playershuffle", "true", 0, False
    )


async def test_cmd_shuffle_false(
        hass, mqtt_client_mock, mqtt_mock, mock_phoniebox, config, media_player_entry
):
    data = {ATTR_ENTITY_ID: media_player_entry.entity_id, ATTR_MEDIA_SHUFFLE: "false"}
    await hass.services.async_call(
        "media_player", SERVICE_SHUFFLE_SET, data, blocking=True
    )
    mqtt_mock.async_publish.assert_called_once_with(
        "test_phoniebox/cmd/playershuffle", "false", 0, False
    )


async def test_cmd_repeat_all(
        hass, mqtt_client_mock, mqtt_mock, mock_phoniebox, config, media_player_entry
):
    data = {
        ATTR_ENTITY_ID: media_player_entry.entity_id,
        ATTR_MEDIA_REPEAT: REPEAT_MODE_ALL,
    }
    await hass.services.async_call(
        "media_player", SERVICE_REPEAT_SET, data, blocking=True
    )
    mqtt_mock.async_publish.assert_called_once_with(
        "test_phoniebox/cmd/playerrepeat", PHONIEBOX_REPEAT_PLAYLIST, 0, False
    )


async def test_cmd_repeat_single(
        hass, mqtt_client_mock, mqtt_mock, mock_phoniebox, config, media_player_entry
):
    data = {
        ATTR_ENTITY_ID: media_player_entry.entity_id,
        ATTR_MEDIA_REPEAT: REPEAT_MODE_ONE,
    }
    await hass.services.async_call(
        "media_player", SERVICE_REPEAT_SET, data, blocking=True
    )
    mqtt_mock.async_publish.assert_called_once_with(
        "test_phoniebox/cmd/playerrepeat", PHONIEBOX_REPEAT_SINGLE, 0, False
    )


async def test_cmd_repeat_off(
        hass, mqtt_client_mock, mqtt_mock, mock_phoniebox, config, media_player_entry
):
    data = {
        ATTR_ENTITY_ID: media_player_entry.entity_id,
        ATTR_MEDIA_REPEAT: REPEAT_MODE_OFF,
    }
    await hass.services.async_call(
        "media_player", SERVICE_REPEAT_SET, data, blocking=True
    )
    mqtt_mock.async_publish.assert_called_once_with(
        "test_phoniebox/cmd/playerrepeat", PHONIEBOX_REPEAT_OFF, 0, False
    )


async def test_cmd_turn_off(
        hass, mqtt_client_mock, mqtt_mock, mock_phoniebox, config, media_player_entry
):
    data = {ATTR_ENTITY_ID: media_player_entry.entity_id}
    await hass.services.async_call(
        "media_player", SERVICE_TURN_OFF, data, blocking=True
    )
    mqtt_mock.async_publish.assert_called_once_with(
        "test_phoniebox/cmd/shutdown", "{}", 0, False
    )


async def test_cmd_set_vol_level_50(
        hass, mqtt_client_mock, mqtt_mock, mock_phoniebox, config, media_player_entry
):
    data = {ATTR_ENTITY_ID: media_player_entry.entity_id, ATTR_MEDIA_VOLUME_LEVEL: 0.5}
    await hass.services.async_call(
        "media_player", SERVICE_VOLUME_SET, data, blocking=True
    )
    mqtt_mock.async_publish.assert_called_once_with(
        "test_phoniebox/cmd/setvolume", "50", 0, False
    )


async def test_cmd_set_vol_level_100(
        hass, mqtt_client_mock, mqtt_mock, mock_phoniebox, config, media_player_entry
):
    data = {ATTR_ENTITY_ID: media_player_entry.entity_id, ATTR_MEDIA_VOLUME_LEVEL: 1}
    await hass.services.async_call(
        "media_player", SERVICE_VOLUME_SET, data, blocking=True
    )
    mqtt_mock.async_publish.assert_called_once_with(
        "test_phoniebox/cmd/setvolume", "100", 0, False
    )


async def test_cmd_set_vol_level_23(
        hass, mqtt_client_mock, mqtt_mock, mock_phoniebox, config, media_player_entry
):
    data = {ATTR_ENTITY_ID: media_player_entry.entity_id, ATTR_MEDIA_VOLUME_LEVEL: 0.23}
    await hass.services.async_call(
        "media_player", SERVICE_VOLUME_SET, data, blocking=True
    )
    mqtt_mock.async_publish.assert_called_once_with(
        "test_phoniebox/cmd/setvolume", "23", 0, False
    )


async def test_player_states(hass, mqtt_client_mock, mqtt_mock, mock_phoniebox, config):
    # Initial State
    phoniebox_state = hass.states.get("media_player.phoniebox_test_box")
    assert phoniebox_state.state == STATE_UNAVAILABLE

    # Playing State
    async_fire_mqtt_message(hass, "test_phoniebox/attribute/state", "play")
    await hass.async_block_till_done()
    phoniebox_state = hass.states.get("media_player.phoniebox_test_box")
    assert phoniebox_state.state == STATE_PLAYING

    # Paused State
    async_fire_mqtt_message(hass, "test_phoniebox/attribute/state", "pause")
    await hass.async_block_till_done()
    phoniebox_state = hass.states.get("media_player.phoniebox_test_box")
    assert phoniebox_state.state == STATE_PAUSED

    # Stopped State
    async_fire_mqtt_message(hass, "test_phoniebox/attribute/state", "stop")
    await hass.async_block_till_done()
    phoniebox_state = hass.states.get("media_player.phoniebox_test_box")
    assert phoniebox_state.state == STATE_IDLE


async def test_player_volume(hass, mqtt_client_mock, mqtt_mock, mock_phoniebox, config):
    # Initial State
    phoniebox_state = hass.states.get("media_player.phoniebox_test_box")
    assert phoniebox_state.attributes.get(ATTR_MEDIA_VOLUME_LEVEL) == 0.0

    # Various volume changes
    async_fire_mqtt_message(hass, "test_phoniebox/attribute/volume", "5")
    await hass.async_block_till_done()
    phoniebox_state = hass.states.get("media_player.phoniebox_test_box")
    assert phoniebox_state.attributes.get(ATTR_MEDIA_VOLUME_LEVEL) == 0.05

    async_fire_mqtt_message(hass, "test_phoniebox/attribute/volume", "50")
    await hass.async_block_till_done()
    phoniebox_state = hass.states.get("media_player.phoniebox_test_box")
    assert phoniebox_state.attributes.get(ATTR_MEDIA_VOLUME_LEVEL) == 0.5

    async_fire_mqtt_message(hass, "test_phoniebox/attribute/volume", "100")
    await hass.async_block_till_done()
    phoniebox_state = hass.states.get("media_player.phoniebox_test_box")
    assert phoniebox_state.attributes.get(ATTR_MEDIA_VOLUME_LEVEL) == 1.0

    async_fire_mqtt_message(hass, "test_phoniebox/attribute/volume", "0")
    await hass.async_block_till_done()
    phoniebox_state = hass.states.get("media_player.phoniebox_test_box")
    assert phoniebox_state.attributes.get(ATTR_MEDIA_VOLUME_LEVEL) == 0.0

    async_fire_mqtt_message(hass, "test_phoniebox/attribute/volume", "15")
    await hass.async_block_till_done()
    phoniebox_state = hass.states.get("media_player.phoniebox_test_box")
    assert phoniebox_state.attributes.get(ATTR_MEDIA_VOLUME_LEVEL) == 0.15

    async_fire_mqtt_message(hass, "test_phoniebox/attribute/volume", "1.5")
    await hass.async_block_till_done()
    phoniebox_state = hass.states.get("media_player.phoniebox_test_box")
    assert phoniebox_state.attributes.get(ATTR_MEDIA_VOLUME_LEVEL) == 0.015

    async_fire_mqtt_message(hass, "test_phoniebox/attribute/volume", ".5")
    await hass.async_block_till_done()
    phoniebox_state = hass.states.get("media_player.phoniebox_test_box")
    assert phoniebox_state.attributes.get(ATTR_MEDIA_VOLUME_LEVEL) == 0.005


async def test_player_mute(hass, mqtt_client_mock, mqtt_mock, mock_phoniebox, config):
    # Initial State
    phoniebox_state = hass.states.get("media_player.phoniebox_test_box")
    assert phoniebox_state.attributes.get(ATTR_MEDIA_VOLUME_MUTED) is False

    # Mute the box
    async_fire_mqtt_message(hass, "test_phoniebox/attribute/mute", "true")
    await hass.async_block_till_done()
    phoniebox_state = hass.states.get("media_player.phoniebox_test_box")
    assert phoniebox_state.attributes.get(ATTR_MEDIA_VOLUME_MUTED) is True

    # Unmute
    async_fire_mqtt_message(hass, "test_phoniebox/attribute/mute", "false")
    await hass.async_block_till_done()
    phoniebox_state = hass.states.get("media_player.phoniebox_test_box")
    assert phoniebox_state.attributes.get(ATTR_MEDIA_VOLUME_MUTED) is False


async def test_shuffle(hass, mqtt_client_mock, mqtt_mock, mock_phoniebox, config):
    # Initial State
    phoniebox_state = hass.states.get("media_player.phoniebox_test_box")
    assert phoniebox_state.attributes.get("shuffle") is False

    async_fire_mqtt_message(hass, "test_phoniebox/attribute/random", "true")
    await hass.async_block_till_done()
    phoniebox_state = hass.states.get("media_player.phoniebox_test_box")
    assert phoniebox_state.attributes.get(ATTR_MEDIA_SHUFFLE) is True

    async_fire_mqtt_message(hass, "test_phoniebox/attribute/random", "false")
    await hass.async_block_till_done()
    phoniebox_state = hass.states.get("media_player.phoniebox_test_box")
    assert phoniebox_state.attributes.get(ATTR_MEDIA_SHUFFLE) is False


async def test_duration(hass, mqtt_client_mock, mqtt_mock, mock_phoniebox, config):
    # Initial State
    phoniebox_state = hass.states.get("media_player.phoniebox_test_box")
    assert phoniebox_state.attributes.get(ATTR_MEDIA_DURATION) == 0

    async_fire_mqtt_message(hass, "test_phoniebox/attribute/duration", "00:00:55")
    await hass.async_block_till_done()
    phoniebox_state = hass.states.get("media_player.phoniebox_test_box")
    assert phoniebox_state.attributes.get(ATTR_MEDIA_DURATION) == 55

    async_fire_mqtt_message(hass, "test_phoniebox/attribute/duration", "01:32:55")
    await hass.async_block_till_done()
    phoniebox_state = hass.states.get("media_player.phoniebox_test_box")
    assert phoniebox_state.attributes.get(ATTR_MEDIA_DURATION) == 5575

    async_fire_mqtt_message(hass, "test_phoniebox/attribute/duration", "00:00:00")
    await hass.async_block_till_done()
    phoniebox_state = hass.states.get("media_player.phoniebox_test_box")
    assert phoniebox_state.attributes.get(ATTR_MEDIA_DURATION) == 0


async def test_track(hass, mqtt_client_mock, mqtt_mock, mock_phoniebox, config):
    # Initial State
    phoniebox_state = hass.states.get("media_player.phoniebox_test_box")
    assert phoniebox_state.attributes.get(ATTR_MEDIA_TRACK) is None

    async_fire_mqtt_message(hass, "test_phoniebox/attribute/track", "12333")
    await hass.async_block_till_done()
    phoniebox_state = hass.states.get("media_player.phoniebox_test_box")
    assert phoniebox_state.attributes.get(ATTR_MEDIA_TRACK) == 12333

    async_fire_mqtt_message(hass, "test_phoniebox/attribute/track", "0")
    await hass.async_block_till_done()
    phoniebox_state = hass.states.get("media_player.phoniebox_test_box")
    assert phoniebox_state.attributes.get(ATTR_MEDIA_TRACK) == 0


async def test_elapsed(hass, mqtt_client_mock, mqtt_mock, mock_phoniebox, config):
    # Initial State
    phoniebox_state = hass.states.get("media_player.phoniebox_test_box")
    assert phoniebox_state.attributes.get(ATTR_MEDIA_POSITION) == 0

    async_fire_mqtt_message(hass, "test_phoniebox/attribute/elapsed", "00:00:55")
    await hass.async_block_till_done()
    phoniebox_state = hass.states.get("media_player.phoniebox_test_box")
    assert phoniebox_state.attributes.get(ATTR_MEDIA_POSITION) == 55

    async_fire_mqtt_message(hass, "test_phoniebox/attribute/elapsed", "01:32:55")
    await hass.async_block_till_done()
    phoniebox_state = hass.states.get("media_player.phoniebox_test_box")
    assert phoniebox_state.attributes.get(ATTR_MEDIA_POSITION) == 5575

    async_fire_mqtt_message(hass, "test_phoniebox/attribute/elapsed", "00:00:00")
    await hass.async_block_till_done()
    phoniebox_state = hass.states.get("media_player.phoniebox_test_box")
    assert phoniebox_state.attributes.get(ATTR_MEDIA_POSITION) == 0


async def test_artist(hass, mqtt_client_mock, mqtt_mock, mock_phoniebox, config):
    # Initial State
    phoniebox_state = hass.states.get("media_player.phoniebox_test_box")
    assert phoniebox_state.attributes.get(ATTR_MEDIA_ARTIST) is None

    async_fire_mqtt_message(hass, "test_phoniebox/attribute/artist", "Artist")
    await hass.async_block_till_done()
    phoniebox_state = hass.states.get("media_player.phoniebox_test_box")
    assert phoniebox_state.attributes.get(ATTR_MEDIA_ARTIST) == "Artist"

    async_fire_mqtt_message(hass, "test_phoniebox/attribute/artist", "Artist2")
    await hass.async_block_till_done()
    phoniebox_state = hass.states.get("media_player.phoniebox_test_box")
    assert phoniebox_state.attributes.get(ATTR_MEDIA_ARTIST) == "Artist2"


async def test_title(hass, mqtt_client_mock, mqtt_mock, mock_phoniebox, config):
    # Initial State
    phoniebox_state = hass.states.get("media_player.phoniebox_test_box")
    assert phoniebox_state.attributes.get(ATTR_MEDIA_TITLE) is None

    async_fire_mqtt_message(hass, "test_phoniebox/attribute/title", "Awesome Title")
    await hass.async_block_till_done()
    phoniebox_state = hass.states.get("media_player.phoniebox_test_box")
    assert phoniebox_state.attributes.get(ATTR_MEDIA_TITLE) == "Awesome Title"

    async_fire_mqtt_message(hass, "test_phoniebox/attribute/title", "Awesome Title 2")
    await hass.async_block_till_done()
    phoniebox_state = hass.states.get("media_player.phoniebox_test_box")
    assert phoniebox_state.attributes.get(ATTR_MEDIA_TITLE) == "Awesome Title 2"


async def test_album(hass, mqtt_client_mock, mqtt_mock, mock_phoniebox, config):
    # Initial State
    phoniebox_state = hass.states.get("media_player.phoniebox_test_box")
    assert phoniebox_state.attributes.get(ATTR_MEDIA_ALBUM_NAME) is None

    async_fire_mqtt_message(hass, "test_phoniebox/attribute/album", "Awesome album")
    await hass.async_block_till_done()
    phoniebox_state = hass.states.get("media_player.phoniebox_test_box")
    assert phoniebox_state.attributes.get(ATTR_MEDIA_ALBUM_NAME) == "Awesome album"

    async_fire_mqtt_message(hass, "test_phoniebox/attribute/album", "Awesome album 2")
    await hass.async_block_till_done()
    phoniebox_state = hass.states.get("media_player.phoniebox_test_box")
    assert phoniebox_state.attributes.get(ATTR_MEDIA_ALBUM_NAME) == "Awesome album 2"


async def test_repeat(hass, mqtt_client_mock, mqtt_mock, mock_phoniebox, config):
    # Initial State
    phoniebox_state = hass.states.get("media_player.phoniebox_test_box")
    assert phoniebox_state.attributes.get(ATTR_MEDIA_REPEAT) == REPEAT_MODE_OFF

    async_fire_mqtt_message(hass, "test_phoniebox/attribute/repeat", "true")
    await hass.async_block_till_done()
    phoniebox_state = hass.states.get("media_player.phoniebox_test_box")
    assert phoniebox_state.attributes.get(ATTR_MEDIA_REPEAT) == REPEAT_MODE_ONE

    async_fire_mqtt_message(hass, "test_phoniebox/attribute/repeat", "false")
    await hass.async_block_till_done()
    phoniebox_state = hass.states.get("media_player.phoniebox_test_box")
    assert phoniebox_state.attributes.get(ATTR_MEDIA_REPEAT) == REPEAT_MODE_OFF
