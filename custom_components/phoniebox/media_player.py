"""BlueprintEntity class"""
import logging
from abc import ABC, ABCMeta

from homeassistant.components.media_player import MediaPlayerEntity
from homeassistant.components.media_player.const import (
    MEDIA_TYPE_MUSIC,
    REPEAT_MODE_OFF,
    REPEAT_MODE_ONE,
)
from homeassistant.const import STATE_IDLE

from .const import (
    ATTRIBUTION,
    CONF_PHONIEBOX_NAME,
    DOMAIN,
    HA_REPEAT_TO_PHONIEBOX,
    NAME,
    PHONIEBOX_STATE_TO_HA,
    SUPPORT_MQTTMEDIAPLAYER,
    VERSION,
)
from .sensor import string_to_bool

_LOGGER: logging.Logger = logging.getLogger(__package__)


async def async_setup_entry(hass, entry, async_add_devices):
    """Setup media player platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_devices([IntegrationBlueprintMediaPlayer(coordinator, entry, hass)])

    platform = entry.async_get_current_platform()
    platform.async_register_entity_service(
        SERVICE_SET_TIMER,
        {
            vol.Required('sleep_time'): cv.time_period,
        },
        "set_sleep_timer",
    )


class IntegrationBlueprintMediaPlayer(MediaPlayerEntity, ABC):
    _attr_should_poll = False
    _attr_media_content_type = MEDIA_TYPE_MUSIC
    _attr_supported_features = SUPPORT_MQTTMEDIAPLAYER

    def __init__(self, coordinator, config_entry, hass):
        _LOGGER.debug("media player __init__")

        self.config_entry = config_entry
        self.coordinator = coordinator
        self.mqtt_client = coordinator.mqtt_client
        self._attr_name = "Phoniebox " + config_entry.data[CONF_PHONIEBOX_NAME]
        self._attr_unique_id = self.config_entry.entry_id
        self._attr_state = STATE_IDLE
        self._attr_volume_level = 0.0
        self._attr_is_volume_muted = False
        self._attr_shuffle = False
        self._attr_repeat = REPEAT_MODE_OFF
        self._max_volume = 100
        self._attr_media_artist = None
        self._attr_media_album_artist = None
        self._attr_media_album_name = None
        self._attr_media_title = None
        self._attr_media_track = None
        self._vol_steps = 5

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self.unique_id)},
            "name": NAME,
            "model": VERSION,
            "manufacturer": NAME,
        }

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return {
            "attribution": ATTRIBUTION,
            "id": self.config_entry.entry_id,
            "integration": DOMAIN,
        }

    async def async_set_attributes(self, msg):
        """Set volume level."""
        # _LOGGER.debug('async_set_attributes ----> %s', msg)

        changed_attribute_name = msg.topic.split("/")[2]
        new_value = msg.payload
        if changed_attribute_name == "volume":
            self._attr_volume_level = float(new_value) / 100.0
        elif changed_attribute_name == "state":
            self._attr_state = PHONIEBOX_STATE_TO_HA[new_value]
        elif changed_attribute_name == "mute":
            self._attr_is_volume_muted = string_to_bool(new_value)
        elif changed_attribute_name == "random":
            self._attr_shuffle = string_to_bool(new_value)
        elif changed_attribute_name == "maxvolume":
            self._max_volume = float(new_value)
        elif changed_attribute_name == "duration":
            self._attr_media_duration = sum(
                x * int(t) for x, t in zip([3600, 60, 1], new_value.split(":"))
            )
        elif changed_attribute_name == "track":
            self._attr_media_track = int(new_value)
        elif changed_attribute_name == "elapsed":
            self._attr_media_position = sum(
                x * int(t) for x, t in zip([3600, 60, 1], new_value.split(":"))
            )
        elif changed_attribute_name == "artist":
            self._attr_media_artist = new_value
        elif changed_attribute_name == "title":
            self._attr_media_title = new_value
        elif changed_attribute_name == "album":
            self._attr_media_album_name = new_value
        elif changed_attribute_name == "albumartist":
            self._attr_media_album_artist = new_value
        elif changed_attribute_name == "volstep":
            self._vol_steps = new_value
        elif changed_attribute_name == "repeat":
            if new_value == "true":
                self._attr_repeat = REPEAT_MODE_ONE  # is bad but phoniebox will only say if repeat is on or off
            else:
                self._attr_repeat = REPEAT_MODE_OFF

        self.schedule_update_ha_state(True)

    async def async_added_to_hass(self):
        """Subscribe to MQTT events."""
        await self.mqtt_client.async_subscribe("attribute/#", self.async_set_attributes)

    async def async_volume_up(self):
        """Volume up the media player."""
        await self.mqtt_client.async_publish("cmd/volumeup", {})

    async def async_volume_down(self):
        """Volume up the media player."""
        await self.mqtt_client.async_publish("cmd/volumedown", {})

    async def async_mute_volume(self, mute):
        """Send the media player the command for muting the volume."""
        _LOGGER.debug("mute: %s", mute)
        await self.mqtt_client.async_publish("cmd/mute", mute)

    async def async_media_play(self):
        """Send play command."""
        await self.mqtt_client.async_publish("cmd/playerplay", {})

    async def async_media_pause(self):
        """Send pause command."""
        await self.mqtt_client.async_publish("cmd/playerpause", {})

    async def async_media_stop(self):
        """Send stop command."""
        await self.mqtt_client.async_publish("cmd/playerstop", {})

    async def async_media_previous_track(self):
        """Send previous track command."""
        await self.mqtt_client.async_publish("cmd/playerprev", {})

    async def async_media_next_track(self):
        """Send next track command."""
        await self.mqtt_client.async_publish("cmd/playernext", {})

    async def async_media_seek(self, position):
        """Send seek command."""
        _LOGGER.debug("position: %s", position)
        await self.mqtt_client.async_publish("cmd/playerseek", position)

    async def async_set_shuffle(self, shuffle):
        """Enable/disable shuffle mode."""
        _LOGGER.debug("shuffle: %s", shuffle)
        await self.mqtt_client.async_publish("cmd/playershuffle", shuffle)

    async def async_set_repeat(self, repeat):
        """Set repeat mode."""
        _LOGGER.debug("repeat: %s", repeat)
        await self.mqtt_client.async_publish(
            "cmd/playerrepeat", HA_REPEAT_TO_PHONIEBOX[repeat]
        )

    async def async_turn_off(self):
        """Turn the media player off."""
        await self.mqtt_client.async_publish("cmd/shutdown", {})

    async def async_set_volume_level(self, volume):
        """Set volume level, range 0..1."""
        await self.mqtt_client.async_publish("cmd/setvolume", int(volume * 100))
