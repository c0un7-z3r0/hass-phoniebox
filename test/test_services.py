from homeassistant.components.media_player import ATTR_MEDIA_SEEK_POSITION
from homeassistant.const import SERVICE_VOLUME_DOWN, ATTR_ENTITY_ID, ATTR_TIME

from custom_components.phoniebox.const import (
    SUPPORT_MQTTMEDIAPLAYER, ATTR_VOLUME_STEPS, DOMAIN, SERVICE_VOLUME_STEPS,
    ATTR_MAX_VOLUME, SERVICE_MAX_VOLUME, SERVICE_IDLE_TIMER, ATTR_IDLE_TIME,
    SERVICE_SHUTDOWN_AFTER,
    SERVICE_SLEEP_TIMER, SERVICE_RFID, ATTR_IS_STARTED, SERVICE_GPIO,
    SERVICE_SWIPE_CARD, SERVICE_PLAY_FOLDER,
    SERVICE_PLAY_FOLDER_RECURSIVE, SERVICE_PLAYER_SEEK, SERVICE_REWIND,
    SERVICE_REPLAY, SERVICE_SCAN,
    SERVICE_TURN_OFF_SILENT, SERVICE_RESTART, SERVICE_DISABLE_WIFI, ATTR_CARD_ID, ATTR_FOLDER_NAME
)


async def test_service_volume_steps(
        hass, mqtt_client_mock, mqtt_mock, mock_phoniebox, config, media_player_entry
):
    data = {ATTR_ENTITY_ID: media_player_entry.entity_id, ATTR_VOLUME_STEPS: 3}
    await hass.services.async_call(
        DOMAIN, SERVICE_VOLUME_STEPS, data, blocking=True
    )
    mqtt_mock.async_publish.assert_called_once_with(
        "test_phoniebox/cmd/setvolstep", "3", 0, False
    )


async def test_service_max_volume(
        hass, mqtt_client_mock, mqtt_mock, mock_phoniebox, config, media_player_entry
):
    data = {ATTR_ENTITY_ID: media_player_entry.entity_id, ATTR_MAX_VOLUME: 30}
    await hass.services.async_call(
        DOMAIN, SERVICE_MAX_VOLUME, data, blocking=True
    )
    mqtt_mock.async_publish.assert_called_once_with(
        "test_phoniebox/cmd/setmaxvolume", "30", 0, False
    )


async def test_service_idle_time(
        hass, mqtt_client_mock, mqtt_mock, mock_phoniebox, config, media_player_entry
):
    data = {ATTR_ENTITY_ID: media_player_entry.entity_id, ATTR_TIME: 60}
    await hass.services.async_call(
        DOMAIN, SERVICE_IDLE_TIMER, data, blocking=True
    )
    mqtt_mock.async_publish.assert_called_once_with(
        "test_phoniebox/cmd/setidletime", "60", 0, False
    )


async def test_service_shutdown_after(
        hass, mqtt_client_mock, mqtt_mock, mock_phoniebox, config, media_player_entry
):
    data = {ATTR_ENTITY_ID: media_player_entry.entity_id, ATTR_TIME: 32}
    await hass.services.async_call(
        DOMAIN, SERVICE_SHUTDOWN_AFTER, data, blocking=True
    )
    mqtt_mock.async_publish.assert_called_once_with(
        "test_phoniebox/cmd/shutdownafter", "32", 0, False
    )


async def test_service_sleep_timer(
        hass, mqtt_client_mock, mqtt_mock, mock_phoniebox, config, media_player_entry
):
    data = {ATTR_ENTITY_ID: media_player_entry.entity_id, ATTR_TIME: 32}
    await hass.services.async_call(
        DOMAIN, SERVICE_SLEEP_TIMER, data, blocking=True
    )
    mqtt_mock.async_publish.assert_called_once_with(
        "test_phoniebox/cmd/playerstopafter", "32", 0, False
    )


async def test_service_start_rfid(
        hass, mqtt_client_mock, mqtt_mock, mock_phoniebox, config, media_player_entry
):
    data = {ATTR_ENTITY_ID: media_player_entry.entity_id, ATTR_IS_STARTED: True}
    await hass.services.async_call(
        DOMAIN, SERVICE_RFID, data, blocking=True
    )
    mqtt_mock.async_publish.assert_called_once_with(
        "test_phoniebox/cmd/rfid", "start", 0, False
    )


async def test_service_stop_rfid(
        hass, mqtt_client_mock, mqtt_mock, mock_phoniebox, config, media_player_entry
):
    data = {ATTR_ENTITY_ID: media_player_entry.entity_id, ATTR_IS_STARTED: False}
    await hass.services.async_call(
        DOMAIN, SERVICE_RFID, data, blocking=True
    )
    mqtt_mock.async_publish.assert_called_once_with(
        "test_phoniebox/cmd/rfid", "stop", 0, False
    )


async def test_service_start_gpio(
        hass, mqtt_client_mock, mqtt_mock, mock_phoniebox, config, media_player_entry
):
    data = {ATTR_ENTITY_ID: media_player_entry.entity_id, ATTR_IS_STARTED: True}
    await hass.services.async_call(
        DOMAIN, SERVICE_GPIO, data, blocking=True
    )
    mqtt_mock.async_publish.assert_called_once_with(
        "test_phoniebox/cmd/gpio", "start", 0, False
    )


async def test_service_stop_gpio(
        hass, mqtt_client_mock, mqtt_mock, mock_phoniebox, config, media_player_entry
):
    data = {ATTR_ENTITY_ID: media_player_entry.entity_id, ATTR_IS_STARTED: False}
    await hass.services.async_call(
        DOMAIN, SERVICE_GPIO, data, blocking=True
    )
    mqtt_mock.async_publish.assert_called_once_with(
        "test_phoniebox/cmd/gpio", "stop", 0, False
    )

async def test_service_swipe_card(
        hass, mqtt_client_mock, mqtt_mock, mock_phoniebox, config, media_player_entry
):
    data = {ATTR_ENTITY_ID: media_player_entry.entity_id, ATTR_CARD_ID: "06438323"}
    await hass.services.async_call(
        DOMAIN, SERVICE_SWIPE_CARD, data, blocking=True
    )
    mqtt_mock.async_publish.assert_called_once_with(
        "test_phoniebox/cmd/swipecard", "06438323", 0, False
    )

async def test_service_play_folder(
        hass, mqtt_client_mock, mqtt_mock, mock_phoniebox, config, media_player_entry
):
    data = {ATTR_ENTITY_ID: media_player_entry.entity_id, ATTR_FOLDER_NAME: "audiobook"}
    await hass.services.async_call(
        DOMAIN, SERVICE_PLAY_FOLDER, data, blocking=True
    )
    mqtt_mock.async_publish.assert_called_once_with(
        "test_phoniebox/cmd/playfolder", "audiobook", 0, False
    )

async def test_service_play_folder_recursive(
        hass, mqtt_client_mock, mqtt_mock, mock_phoniebox, config, media_player_entry
):
    data = {ATTR_ENTITY_ID: media_player_entry.entity_id, ATTR_FOLDER_NAME: "audiobook"}
    await hass.services.async_call(
        DOMAIN, SERVICE_PLAY_FOLDER_RECURSIVE, data, blocking=True
    )
    mqtt_mock.async_publish.assert_called_once_with(
        "test_phoniebox/cmd/playfolderrecursive", "audiobook", 0, False
    )

async def test_service_player_seek_forward(
        hass, mqtt_client_mock, mqtt_mock, mock_phoniebox, config, media_player_entry
):
    data = {ATTR_ENTITY_ID: media_player_entry.entity_id, ATTR_MEDIA_SEEK_POSITION: "20"}
    await hass.services.async_call(
        DOMAIN, SERVICE_PLAYER_SEEK, data, blocking=True
    )
    mqtt_mock.async_publish.assert_called_once_with(
        "test_phoniebox/cmd/playerseek", "20", 0, False
    )

async def test_service_player_seek_backwards(
        hass, mqtt_client_mock, mqtt_mock, mock_phoniebox, config, media_player_entry
):
    data = {ATTR_ENTITY_ID: media_player_entry.entity_id, ATTR_MEDIA_SEEK_POSITION: "-20"}
    await hass.services.async_call(
        DOMAIN, SERVICE_PLAYER_SEEK, data, blocking=True
    )
    mqtt_mock.async_publish.assert_called_once_with(
        "test_phoniebox/cmd/playerseek", "-20", 0, False
    )

async def test_service_rewind(
        hass, mqtt_client_mock, mqtt_mock, mock_phoniebox, config, media_player_entry
):
    data = {ATTR_ENTITY_ID: media_player_entry.entity_id}
    await hass.services.async_call(
        DOMAIN, SERVICE_REWIND, data, blocking=True
    )
    mqtt_mock.async_publish.assert_called_once_with(
        "test_phoniebox/cmd/playerrewind", "{}", 0, False
    )

async def test_service_replay(
        hass, mqtt_client_mock, mqtt_mock, mock_phoniebox, config, media_player_entry
):
    data = {ATTR_ENTITY_ID: media_player_entry.entity_id}
    await hass.services.async_call(
        DOMAIN, SERVICE_REPLAY, data, blocking=True
    )
    mqtt_mock.async_publish.assert_called_once_with(
        "test_phoniebox/cmd/playerreplay", "{}", 0, False
    )

async def test_service_scan(
        hass, mqtt_client_mock, mqtt_mock, mock_phoniebox, config, media_player_entry
):
    data = {ATTR_ENTITY_ID: media_player_entry.entity_id}
    await hass.services.async_call(
        DOMAIN, SERVICE_SCAN, data, blocking=True
    )
    mqtt_mock.async_publish.assert_called_once_with(
        "test_phoniebox/cmd/scan", "{}", 0, False
    )

async def test_service_turn_off_silent(
        hass, mqtt_client_mock, mqtt_mock, mock_phoniebox, config, media_player_entry
):
    data = {ATTR_ENTITY_ID: media_player_entry.entity_id}
    await hass.services.async_call(
        DOMAIN, SERVICE_TURN_OFF_SILENT, data, blocking=True
    )
    mqtt_mock.async_publish.assert_called_once_with(
        "test_phoniebox/cmd/shutdownsilent", "{}", 0, False
    )

async def test_service_restart(
        hass, mqtt_client_mock, mqtt_mock, mock_phoniebox, config, media_player_entry
):
    data = {ATTR_ENTITY_ID: media_player_entry.entity_id}
    await hass.services.async_call(
        DOMAIN, SERVICE_RESTART, data, blocking=True
    )
    mqtt_mock.async_publish.assert_called_once_with(
        "test_phoniebox/cmd/reboot", "{}", 0, False
    )
