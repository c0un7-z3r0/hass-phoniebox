""" All custom services that can be used with the phoniebox """
import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.components.media_player import ATTR_MEDIA_SEEK_POSITION
from homeassistant.const import ATTR_TIME
from homeassistant.helpers import entity_platform
from homeassistant.helpers.entity_platform import EntityPlatform

from custom_components.phoniebox.const import (
    ATTR_VOLUME_STEPS, SERVICE_VOLUME_STEPS,
    ATTR_MAX_VOLUME, SERVICE_MAX_VOLUME, SERVICE_IDLE_TIMER, SERVICE_SHUTDOWN_AFTER,
    SERVICE_SLEEP_TIMER, SERVICE_RFID, ATTR_IS_STARTED, SERVICE_GPIO,
    SERVICE_SWIPE_CARD, SERVICE_PLAY_FOLDER,
    SERVICE_PLAY_FOLDER_RECURSIVE, SERVICE_PLAYER_SEEK, SERVICE_REWIND,
    SERVICE_REPLAY, SERVICE_SCAN,
    SERVICE_TURN_OFF_SILENT, SERVICE_RESTART, SERVICE_DISABLE_WIFI, ATTR_CARD_ID, ATTR_FOLDER_NAME
)

minutes_int = vol.All(
    vol.Coerce(int),
    vol.Range(min=0, max=60))

percent_int = vol.All(
    vol.Coerce(int),
    vol.Range(min=0, max=100))


async def async_register_custom_services():
    platform: EntityPlatform = entity_platform.async_get_current_platform()

    platform.async_register_entity_service(
        SERVICE_VOLUME_STEPS,
        vol.All(
            cv.make_entity_service_schema(
                {vol.Required(ATTR_VOLUME_STEPS): percent_int}
            ),
        ),
        "async_set_volume_steps",
    )

    platform.async_register_entity_service(
        SERVICE_MAX_VOLUME,
        vol.All(
            cv.make_entity_service_schema(
                {vol.Required(ATTR_MAX_VOLUME): percent_int}
            ),
        ),
        "async_set_max_volume",
    )

    platform.async_register_entity_service(
        SERVICE_IDLE_TIMER,
        vol.All(
            cv.make_entity_service_schema(
                {vol.Required(ATTR_TIME): minutes_int}
            ),
        ),
        "async_set_idle_shutdown_timer",
    )

    platform.async_register_entity_service(
        SERVICE_SHUTDOWN_AFTER,
        vol.All(
            cv.make_entity_service_schema(
                {vol.Required(ATTR_TIME): minutes_int}
            ),
        ),
        "async_set_shutdown_after",
    )

    platform.async_register_entity_service(
        SERVICE_SLEEP_TIMER,
        vol.All(
            cv.make_entity_service_schema(
                {vol.Required(ATTR_TIME): minutes_int}
            ),
        ),
        "async_set_sleep_timer",
    )

    platform.async_register_entity_service(
        SERVICE_RFID,
        vol.All(
            cv.make_entity_service_schema(
                {vol.Required(ATTR_IS_STARTED): cv.boolean}
            ),
        ),
        "async_toggle_rfid",
    )

    platform.async_register_entity_service(
        SERVICE_GPIO,
        vol.All(
            cv.make_entity_service_schema(
                {vol.Required(ATTR_IS_STARTED): cv.boolean}
            ),
        ),
        "async_toggle_gpio",
    )

    platform.async_register_entity_service(
        SERVICE_SWIPE_CARD,
        vol.All(
            cv.make_entity_service_schema(
                {vol.Required(ATTR_CARD_ID): cv.string}
            ),
        ),
        "async_swipe_card",
    )

    platform.async_register_entity_service(
        SERVICE_PLAY_FOLDER,
        vol.All(
            cv.make_entity_service_schema(
                {vol.Required(ATTR_FOLDER_NAME): cv.string}
            ),
        ),
        "async_play_folder",
    )

    platform.async_register_entity_service(
        SERVICE_PLAY_FOLDER_RECURSIVE,
        vol.All(
            cv.make_entity_service_schema(
                {vol.Required(ATTR_FOLDER_NAME): cv.string}
            ),
        ),
        "async_play_folder_recursive",
    )

    platform.async_register_entity_service(
        SERVICE_PLAYER_SEEK,
        vol.All(
            cv.make_entity_service_schema(
                {vol.Required(ATTR_MEDIA_SEEK_POSITION): vol.All(vol.Coerce(int), vol.Range(min=-60, max=60))}
            ),
        ),
        "async_seek",
    )

    platform.async_register_entity_service(SERVICE_REWIND, {}, "async_rewind", )
    platform.async_register_entity_service(SERVICE_REPLAY, {}, "async_replay", )
    platform.async_register_entity_service(SERVICE_SCAN, {}, "async_scan", )
    platform.async_register_entity_service(SERVICE_TURN_OFF_SILENT, {}, "async_turn_off_silent", )
    platform.async_register_entity_service(SERVICE_RESTART, {}, "async_restart", )
    platform.async_register_entity_service(SERVICE_DISABLE_WIFI, {}, "async_disable_wifi", )
