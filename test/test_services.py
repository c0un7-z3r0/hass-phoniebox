from homeassistant.const import SERVICE_VOLUME_DOWN, ATTR_ENTITY_ID

from custom_components.phoniebox.const import SUPPORT_MQTTMEDIAPLAYER, ATTR_VOLUME_STEPS, DOMAIN, SERVICE_VOLUME_STEPS, \
    ATTR_MAX_VOLUME, SERVICE_MAX_VOLUME, SERVICE_IDLE_TIMER, ATTR_IDLE_TIME


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
    data = {ATTR_ENTITY_ID: media_player_entry.entity_id, ATTR_IDLE_TIME: 60}
    await hass.services.async_call(
        DOMAIN, SERVICE_IDLE_TIMER, data, blocking=True
    )
    mqtt_mock.async_publish.assert_called_once_with(
        "test_phoniebox/cmd/setidletime", "60", 0, False
    )
