"""All custom services that can be used with the phoniebox."""

from typing import TYPE_CHECKING

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.components.media_player import ATTR_MEDIA_SEEK_POSITION
from homeassistant.const import ATTR_TIME
from homeassistant.helpers import entity_platform

from custom_components.phoniebox.const import (
    ATTR_CARD_ID,
    ATTR_FOLDER_NAME,
    ATTR_IS_STARTED,
    ATTR_MAX_VOLUME,
    ATTR_VOLUME_STEPS,
    LOGGER,
    SERVICE_GPIO,
    SERVICE_IDLE_TIMER,
    SERVICE_MAX_VOLUME,
    SERVICE_PLAY_FOLDER,
    SERVICE_PLAY_FOLDER_RECURSIVE,
    SERVICE_PLAYER_SEEK,
    SERVICE_REPLAY,
    SERVICE_RESTART,
    SERVICE_REWIND,
    SERVICE_RFID,
    SERVICE_SCAN,
    SERVICE_SHUTDOWN_AFTER,
    SERVICE_SLEEP_TIMER,
    SERVICE_SWIPE_CARD,
    SERVICE_TURN_OFF_SILENT,
    SERVICE_VOLUME_STEPS,
)

if TYPE_CHECKING:
    from homeassistant.helpers.entity_platform import EntityPlatform

minutes_int = vol.All(vol.Coerce(int), vol.Range(min=0, max=60))

percent_int = vol.All(vol.Coerce(int), vol.Range(min=0, max=100))


async def async_register_custom_services() -> None:
    """Register the custom phoniebox service."""
    LOGGER.debug("Registering Phoniebox services")

    platform: EntityPlatform = entity_platform.async_get_current_platform()

    platform.async_register_entity_service(
        name=SERVICE_VOLUME_STEPS,
        schema=cv.make_entity_service_schema(
            {vol.Required(ATTR_VOLUME_STEPS): percent_int}
        ),
        func="async_set_volume_steps",
    )

    platform.async_register_entity_service(
        name=SERVICE_MAX_VOLUME,
        schema=cv.make_entity_service_schema(
            {vol.Required(ATTR_MAX_VOLUME): percent_int}
        ),
        func="async_set_max_volume",
    )

    platform.async_register_entity_service(
        name=SERVICE_IDLE_TIMER,
        schema=cv.make_entity_service_schema({vol.Required(ATTR_TIME): minutes_int}),
        func="async_set_idle_shutdown_timer",
    )

    platform.async_register_entity_service(
        name=SERVICE_SHUTDOWN_AFTER,
        schema=cv.make_entity_service_schema({vol.Required(ATTR_TIME): minutes_int}),
        func="async_set_shutdown_after",
    )

    platform.async_register_entity_service(
        name=SERVICE_SLEEP_TIMER,
        schema=cv.make_entity_service_schema({vol.Required(ATTR_TIME): minutes_int}),
        func="async_set_sleep_timer",
    )

    platform.async_register_entity_service(
        name=SERVICE_RFID,
        schema=cv.make_entity_service_schema(
            {vol.Required(ATTR_IS_STARTED): cv.boolean}
        ),
        func="async_toggle_rfid",
    )

    platform.async_register_entity_service(
        name=SERVICE_GPIO,
        schema=cv.make_entity_service_schema(
            {vol.Required(ATTR_IS_STARTED): cv.boolean}
        ),
        func="async_toggle_gpio",
    )

    platform.async_register_entity_service(
        name=SERVICE_SWIPE_CARD,
        schema=cv.make_entity_service_schema({vol.Required(ATTR_CARD_ID): cv.string}),
        func="async_swipe_card",
    )

    platform.async_register_entity_service(
        name=SERVICE_PLAY_FOLDER,
        schema=cv.make_entity_service_schema(
            {vol.Required(ATTR_FOLDER_NAME): cv.string}
        ),
        func="async_play_folder",
    )

    platform.async_register_entity_service(
        name=SERVICE_PLAY_FOLDER_RECURSIVE,
        schema=cv.make_entity_service_schema(
            {vol.Required(ATTR_FOLDER_NAME): cv.string}
        ),
        func="async_play_folder_recursive",
    )

    platform.async_register_entity_service(
        name=SERVICE_PLAYER_SEEK,
        schema=cv.make_entity_service_schema(
            {
                vol.Required(ATTR_MEDIA_SEEK_POSITION): vol.All(
                    vol.Coerce(int), vol.Range(min=-60, max=60)
                )
            }
        ),
        func="async_seek",
    )

    platform.async_register_entity_service(
        name=SERVICE_REWIND, schema={}, func="async_rewind"
    )
    platform.async_register_entity_service(
        name=SERVICE_REPLAY, schema={}, func="async_replay"
    )
    platform.async_register_entity_service(
        name=SERVICE_SCAN, schema={}, func="async_scan"
    )
    platform.async_register_entity_service(
        name=SERVICE_TURN_OFF_SILENT, schema={}, func="async_turn_off_silent"
    )
    platform.async_register_entity_service(
        name=SERVICE_RESTART, schema={}, func="async_restart"
    )
