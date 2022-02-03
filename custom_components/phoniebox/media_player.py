"""BlueprintEntity class"""
import logging
from abc import ABC

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
    VERSION, TO_PHONIEBOX_START_STOP,
)
from .entity import PhonieboxEntity
from .services import async_register_custom_services
from .utils import bool_to_string, string_to_bool

_LOGGER: logging.Logger = logging.getLogger(__package__)


async def async_setup_entry(hass, entry, async_add_devices):
    """Setup media player platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_devices([IntegrationBlueprintMediaPlayer(coordinator, entry, hass)])
    await async_register_custom_services()


class IntegrationBlueprintMediaPlayer(PhonieboxEntity, MediaPlayerEntity, ABC):
    _attr_should_poll = False
    _attr_media_content_type = MEDIA_TYPE_MUSIC
    _attr_supported_features = SUPPORT_MQTTMEDIAPLAYER

    def __init__(self, coordinator, config_entry, hass):
        super().__init__(config_entry, coordinator)

        self._attr_name = "Phoniebox " + config_entry.data[CONF_PHONIEBOX_NAME]
        self._attr_state = STATE_IDLE
        self._attr_volume_level = 0.0
        self._attr_media_duration = 0
        self._attr_media_position = 0
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
    def max_volume(self):
        return self._max_volume

    async def async_set_attributes(self, msg):
        """Set volume level."""
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
        await self.mqtt_client.async_publish("cmd/mute", bool_to_string(mute))

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
        await self.mqtt_client.async_publish("cmd/playerseek", position)

    async def async_set_shuffle(self, shuffle):
        """Enable/disable shuffle mode."""
        await self.mqtt_client.async_publish(
            "cmd/playershuffle", bool_to_string(shuffle)
        )

    async def async_set_repeat(self, repeat):
        """Set repeat mode."""
        await self.mqtt_client.async_publish(
            "cmd/playerrepeat", HA_REPEAT_TO_PHONIEBOX[repeat]
        )

    async def async_turn_off(self):
        """Turn the media player off."""
        await self.mqtt_client.async_publish("cmd/shutdown", {})

    async def async_set_volume_level(self, volume):
        """Set volume level, range 0..1."""
        await self.mqtt_client.async_publish("cmd/setvolume", int(volume * 100))

    async def async_set_volume_steps(self, volume_steps):
        """Set volume steps, range 0..100."""
        await self.mqtt_client.async_publish("cmd/setvolstep", volume_steps)

    async def async_set_max_volume(self, max_volume):
        """Set max volume, range 0..100."""
        await self.mqtt_client.async_publish("cmd/setmaxvolume", max_volume)

    async def async_set_idle_shutdown_timer(self, time):
        """Set timer when box is idle to shut down after, in minutes, range 0..60."""
        await self.mqtt_client.async_publish("cmd/setidletime", time)

    async def async_set_shutdown_after(self, time):
        """Set timer to shut down the box, in minutes, range 0..60."""
        await self.mqtt_client.async_publish("cmd/shutdownafter", time)

    async def async_set_sleep_timer(self, time):
        """Set timer to pause the box, in minutes, range 0..60."""
        await self.mqtt_client.async_publish("cmd/playerstopafter", time)

    async def async_toggle_rfid(self, is_started):
        """Start or stop the rfid service."""
        await self.mqtt_client.async_publish("cmd/rfid", TO_PHONIEBOX_START_STOP[bool_to_string(is_started)])

    async def async_toggle_gpio(self, is_started):
        """Start or stop the gpio service."""
        await self.mqtt_client.async_publish("cmd/gpio", TO_PHONIEBOX_START_STOP[bool_to_string(is_started)])

    async def async_swipe_card(self, card_id):
        """Swipe a card id."""
        await self.mqtt_client.async_publish("cmd/swipecard", card_id)

    async def async_play_folder(self, folder_name):
        """Play a folder. Important needs folder name not path."""
        await self.mqtt_client.async_publish("cmd/playfolder", folder_name)

    async def async_play_folder_recursive(self, folder_name):
        """Play a folder. Important needs folder name not path."""
        await self.mqtt_client.async_publish("cmd/playfolderrecursive", folder_name)

    async def async_seek(self, seek_position):
        """Seek to position"""
        await self.mqtt_client.async_publish("cmd/playerseek", seek_position)

    async def async_rewind(self):
        """Rewind command"""
        await self.mqtt_client.async_publish("cmd/playerrewind", {})

    async def async_replay(self):
        """Replay command"""
        await self.mqtt_client.async_publish("cmd/playerreplay", {})

    async def async_scan(self):
        """Scan command"""
        await self.mqtt_client.async_publish("cmd/scan", {})

    async def async_turn_off_silent(self):
        """Turn the media player off silently."""
        await self.mqtt_client.async_publish("cmd/shutdownsilent", {})

    async def async_restart(self):
        """Restart the media player."""
        await self.mqtt_client.async_publish("cmd/reboot", {})

    async def async_disable_wifi(self):
        """Disables wifi. Not sure if this should be activated"""
        raise NotImplementedError()
        # await self.mqtt_client.async_publish("cmd/disablewifi", {})

