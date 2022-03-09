"""BlueprintEntity class"""
from abc import ABC

from homeassistant.components.media_player import MediaPlayerEntity
from homeassistant.components.media_player.const import (
    MEDIA_TYPE_MUSIC, REPEAT_MODE_OFF, REPEAT_MODE_ONE,
)
from homeassistant.components.mqtt import ReceiveMessage
from homeassistant.const import (STATE_IDLE, STATE_UNAVAILABLE, STATE_OFF)
from homeassistant.util import slugify

from .const import (
    CONF_PHONIEBOX_NAME, DOMAIN, HA_REPEAT_TO_PHONIEBOX, PHONIEBOX_STATE_TO_HA, SUPPORT_MQTTMEDIAPLAYER,
    TO_PHONIEBOX_START_STOP, PHONIEBOX_CMD_SCAN, PHONIEBOX_CMD_REBOOT, PHONIEBOX_CMD_SHUTDOWN_SILENT,
    PHONIEBOX_CMD_PLAYER_REPLAY, PHONIEBOX_CMD_PLAYER_REWIND, PHONIEBOX_CMD_PLAYER_SEEK,
    PHONIEBOX_CMD_PLAY_FOLDER_RECURSIVE, PHONIEBOX_CMD_PLAY_FOLDER, PHONIEBOX_CMD_SWIPE_CARD, PHONIEBOX_CMD_SET_GPIO,
    PHONIEBOX_CMD_SET_RFID, PHONIEBOX_CMD_PLAYER_STOP_AFTER, PHONIEBOX_CMD_SHUTDOWN_AFTER, PHONIEBOX_CMD_SET_IDLE_TIME,
    PHONIEBOX_CMD_SET_MAX_VOLUME, PHONIEBOX_CMD_SET_VOLUME_STEPS, PHONIEBOX_CMD_SET_VOLUME, PHONIEBOX_CMD_SHUTDOWN,
    PHONIEBOX_CMD_PLAYER_REPEAT, PHONIEBOX_CMD_PLAYER_SHUFFLE, PHONIEBOX_CMD_PLAYER_NEXT, PHONIEBOX_CMD_PLAYER_PREV,
    PHONIEBOX_CMD_PLAYER_STOP, PHONIEBOX_CMD_PLAYER_PAUSE, PHONIEBOX_CMD_PLAYER_PLAY, PHONIEBOX_CMD_MUTE,
    PHONIEBOX_CMD_VOLUME_DOWN, PHONIEBOX_CMD_VOLUME_UP,
)
from .entity import PhonieboxEntity
from .services import async_register_custom_services
from .utils import bool_to_string, string_to_bool


async def async_setup_entry(hass, entry, async_add_devices) -> None:
    """Setup media player platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_devices([PhonieboxMediaPlayer(coordinator, entry, hass)])
    await async_register_custom_services()


def _slug(poniebox_name: str) -> str:
    return f"media_player.phoniebox_{slugify(poniebox_name)}"


class PhonieboxMediaPlayer(PhonieboxEntity, MediaPlayerEntity, ABC):
    _attr_should_poll = False
    _attr_media_content_type = MEDIA_TYPE_MUSIC
    _attr_supported_features = SUPPORT_MQTTMEDIAPLAYER

    def __init__(self, coordinator, config_entry, hass) -> None:
        super().__init__(config_entry, coordinator)

        self._attr_name = "Phoniebox " + config_entry.data[CONF_PHONIEBOX_NAME]
        self.entity_id = _slug(config_entry.data[CONF_PHONIEBOX_NAME])
        self._attr_state = STATE_UNAVAILABLE  # initially should be unavailable
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

    async def async_set_attributes(self, msg: ReceiveMessage):
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

    async def update_device_state(self, msg: ReceiveMessage) -> None:
        """update the device state."""
        before_state = self._attr_state
        if msg.payload == "offline":
            self._attr_state = STATE_OFF
        else:
            if self._attr_state in [STATE_OFF, STATE_UNAVAILABLE]:
                self._attr_state = STATE_IDLE

        if before_state != self._attr_state:
            self.schedule_update_ha_state(True)

    async def async_added_to_hass(self) -> None:
        """Subscribe to MQTT events."""
        await self.mqtt_client.async_subscribe("attribute/#", self.async_set_attributes)
        await self.mqtt_client.async_subscribe("state", self.update_device_state)

    async def async_volume_up(self) -> None:
        """Volume up the media player."""
        await self.mqtt_client.async_publish_cmd(PHONIEBOX_CMD_VOLUME_UP, {})

    async def async_volume_down(self) -> None:
        """Volume up the media player."""
        await self.mqtt_client.async_publish_cmd(PHONIEBOX_CMD_VOLUME_DOWN, {})

    async def async_mute_volume(self, mute: bool) -> None:
        """Send the media player the command for muting the volume."""
        await self.mqtt_client.async_publish_cmd(PHONIEBOX_CMD_MUTE, bool_to_string(mute))

    async def async_media_play(self) -> None:
        """Send play command."""
        await self.mqtt_client.async_publish_cmd(PHONIEBOX_CMD_PLAYER_PLAY, {})

    async def async_media_pause(self) -> None:
        """Send pause command."""
        await self.mqtt_client.async_publish_cmd(PHONIEBOX_CMD_PLAYER_PAUSE, {})

    async def async_media_stop(self) -> None:
        """Send stop command."""
        await self.mqtt_client.async_publish_cmd(PHONIEBOX_CMD_PLAYER_STOP, {})

    async def async_media_previous_track(self) -> None:
        """Send previous track command."""
        await self.mqtt_client.async_publish_cmd(PHONIEBOX_CMD_PLAYER_PREV, {})

    async def async_media_next_track(self) -> None:
        """Send next track command."""
        await self.mqtt_client.async_publish_cmd(PHONIEBOX_CMD_PLAYER_NEXT, {})

    async def async_media_seek(self, position: int) -> None:
        """Send seek command."""
        await self.mqtt_client.async_publish_cmd(PHONIEBOX_CMD_PLAYER_SEEK, position)

    async def async_set_shuffle(self, shuffle: bool) -> None:
        """Enable/disable shuffle mode."""
        await self.mqtt_client.async_publish_cmd(
            PHONIEBOX_CMD_PLAYER_SHUFFLE, bool_to_string(shuffle)
        )

    async def async_set_repeat(self, repeat: str) -> None:
        """Set repeat mode."""
        await self.mqtt_client.async_publish_cmd(
            PHONIEBOX_CMD_PLAYER_REPEAT, HA_REPEAT_TO_PHONIEBOX[repeat]
        )

    async def async_turn_off(self) -> None:
        """Turn the media player off."""
        await self.mqtt_client.async_publish_cmd(PHONIEBOX_CMD_SHUTDOWN, {})

    async def async_set_volume_level(self, volume: int) -> None:
        """Set volume level, range 0..1."""
        await self.mqtt_client.async_publish_cmd(PHONIEBOX_CMD_SET_VOLUME, int(volume * 100))

    async def async_set_volume_steps(self, volume_steps: int) -> None:
        """Set volume steps, range 0..100."""
        await self.mqtt_client.async_publish_cmd(PHONIEBOX_CMD_SET_VOLUME_STEPS, volume_steps)

    async def async_set_max_volume(self, max_volume: int) -> None:
        """Set max volume, range 0..100."""
        await self.mqtt_client.async_publish_cmd(PHONIEBOX_CMD_SET_MAX_VOLUME, max_volume)

    async def async_set_idle_shutdown_timer(self, time: int) -> None:
        """Set timer when box is idle to shut down after, in minutes, range 0..60."""
        await self.mqtt_client.async_publish_cmd(PHONIEBOX_CMD_SET_IDLE_TIME, time)

    async def async_set_shutdown_after(self, time: int) -> None:
        """Set timer to shut down the box, in minutes, range 0..60."""
        await self.mqtt_client.async_publish_cmd(PHONIEBOX_CMD_SHUTDOWN_AFTER, time)

    async def async_set_sleep_timer(self, time: int) -> None:
        """Set timer to pause the box, in minutes, range 0..60."""
        await self.mqtt_client.async_publish_cmd(PHONIEBOX_CMD_PLAYER_STOP_AFTER, time)

    async def async_toggle_rfid(self, is_started: bool) -> None:
        """Start or stop the rfid service."""
        await self.mqtt_client.async_publish_cmd(PHONIEBOX_CMD_SET_RFID,
                                                 TO_PHONIEBOX_START_STOP[bool_to_string(is_started)])

    async def async_toggle_gpio(self, is_started: bool) -> None:
        """Start or stop the gpio service."""
        await self.mqtt_client.async_publish_cmd(PHONIEBOX_CMD_SET_GPIO,
                                                 TO_PHONIEBOX_START_STOP[bool_to_string(is_started)])

    async def async_swipe_card(self, card_id: str) -> None:
        """Swipe a card id."""
        await self.mqtt_client.async_publish_cmd(PHONIEBOX_CMD_SWIPE_CARD, card_id)

    async def async_play_folder(self, folder_name: str) -> None:
        """Play a folder. Important needs folder name not path."""
        await self.mqtt_client.async_publish_cmd(PHONIEBOX_CMD_PLAY_FOLDER, folder_name)

    async def async_play_folder_recursive(self, folder_name: str):
        """Play a folder. Important needs folder name not path."""
        await self.mqtt_client.async_publish_cmd(PHONIEBOX_CMD_PLAY_FOLDER_RECURSIVE, folder_name)

    async def async_seek(self, seek_position: int) -> None:
        """Seek to position"""
        await self.mqtt_client.async_publish_cmd(PHONIEBOX_CMD_PLAYER_SEEK, seek_position)

    async def async_rewind(self) -> None:
        """Rewind command"""
        await self.mqtt_client.async_publish_cmd(PHONIEBOX_CMD_PLAYER_REWIND, {})

    async def async_replay(self) -> None:
        """Replay command"""
        await self.mqtt_client.async_publish_cmd(PHONIEBOX_CMD_PLAYER_REPLAY, {})

    async def async_scan(self) -> None:
        """Scan command"""
        await self.mqtt_client.async_publish_cmd(PHONIEBOX_CMD_SCAN, {})

    async def async_turn_off_silent(self) -> None:
        """Turn the media player off silently."""
        await self.mqtt_client.async_publish_cmd(PHONIEBOX_CMD_SHUTDOWN_SILENT, {})

    async def async_restart(self) -> None:
        """Restart the media player."""
        await self.mqtt_client.async_publish_cmd(PHONIEBOX_CMD_REBOOT, {})

    async def async_disable_wifi(self) -> None:
        """Disables wifi. Not sure if this should be activated"""
        raise NotImplementedError()
        # await self.mqtt_client.async_publish_cmd(PHONIEBOX_CMD_DISABLE_WIFI, {})
