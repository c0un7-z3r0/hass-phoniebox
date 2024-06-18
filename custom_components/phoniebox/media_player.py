"""BlueprintEntity class."""

from abc import ABC
from typing import override

from homeassistant.components.media_player import (
    MediaPlayerEntity,
    MediaPlayerEntityFeature,
    MediaPlayerState,
)
from homeassistant.components.media_player.const import (
    MEDIA_TYPE_MUSIC,
    REPEAT_MODE_OFF,
    REPEAT_MODE_ONE,
)
from homeassistant.components.mqtt.models import ReceiveMessage
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import STATE_UNAVAILABLE
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.util import slugify

from .const import (
    CONF_PHONIEBOX_NAME,
    DOMAIN,
    HA_REPEAT_TO_PHONIEBOX,
    LOGGER,
    MEDIA_PLAYER_STATE_UNKNOWN,
    PHONIEBOX_ATTR_ALBUM,
    PHONIEBOX_ATTR_ALBUM_ARTIST,
    PHONIEBOX_ATTR_ARTIST,
    PHONIEBOX_ATTR_DURATION,
    PHONIEBOX_ATTR_ELAPSED,
    PHONIEBOX_ATTR_MAX_VOLUME,
    PHONIEBOX_ATTR_MUTE,
    PHONIEBOX_ATTR_RANDOM,
    PHONIEBOX_ATTR_REPEAT,
    PHONIEBOX_ATTR_STATE,
    PHONIEBOX_ATTR_TITLE,
    PHONIEBOX_ATTR_TRACK,
    PHONIEBOX_ATTR_VOLUME,
    PHONIEBOX_ATTR_VOLUME_STEPS,
    PHONIEBOX_CMD_MUTE,
    PHONIEBOX_CMD_PLAY_FOLDER,
    PHONIEBOX_CMD_PLAY_FOLDER_RECURSIVE,
    PHONIEBOX_CMD_PLAYER_NEXT,
    PHONIEBOX_CMD_PLAYER_PAUSE,
    PHONIEBOX_CMD_PLAYER_PLAY,
    PHONIEBOX_CMD_PLAYER_PREV,
    PHONIEBOX_CMD_PLAYER_REPEAT,
    PHONIEBOX_CMD_PLAYER_REPLAY,
    PHONIEBOX_CMD_PLAYER_REWIND,
    PHONIEBOX_CMD_PLAYER_SEEK,
    PHONIEBOX_CMD_PLAYER_SHUFFLE,
    PHONIEBOX_CMD_PLAYER_STOP,
    PHONIEBOX_CMD_PLAYER_STOP_AFTER,
    PHONIEBOX_CMD_REBOOT,
    PHONIEBOX_CMD_SCAN,
    PHONIEBOX_CMD_SET_GPIO,
    PHONIEBOX_CMD_SET_IDLE_TIME,
    PHONIEBOX_CMD_SET_MAX_VOLUME,
    PHONIEBOX_CMD_SET_RFID,
    PHONIEBOX_CMD_SET_VOLUME,
    PHONIEBOX_CMD_SET_VOLUME_STEPS,
    PHONIEBOX_CMD_SHUTDOWN,
    PHONIEBOX_CMD_SHUTDOWN_AFTER,
    PHONIEBOX_CMD_SHUTDOWN_SILENT,
    PHONIEBOX_CMD_SWIPE_CARD,
    PHONIEBOX_CMD_VOLUME_DOWN,
    PHONIEBOX_CMD_VOLUME_UP,
    PHONIEBOX_STATE_OFFLINE,
    PHONIEBOX_STATE_TO_HA,
    SUPPORT_MQTTMEDIAPLAYER,
    TO_PHONIEBOX_START_STOP,
)
from .data_coordinator import DataCoordinator
from .entity import PhonieboxEntity
from .services import async_register_custom_services
from .utils import bool_to_string, string_to_bool


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set media player platform up."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    LOGGER.debug("📻 Registering media_player")
    media_player = PhonieboxMediaPlayer(coordinator, entry)
    async_add_entities([media_player])
    await async_register_custom_services()


def _slug(phoniebox_name: str) -> str:
    return f"media_player.phoniebox_{slugify(phoniebox_name)}"


class PhonieboxMediaPlayer(PhonieboxEntity, MediaPlayerEntity, ABC):
    """The Phoniebox media player."""

    # pylint: disable=too-many-instance-attributes,too-many-public-methods,too-many-branches
    _attr_should_poll = False
    _attr_media_content_type = MEDIA_TYPE_MUSIC
    _attr_supported_features = MediaPlayerEntityFeature(SUPPORT_MQTTMEDIAPLAYER)

    def __init__(self, coordinator: DataCoordinator, config_entry: ConfigEntry) -> None:
        """Initialise the phoniebox."""
        super().__init__(config_entry, coordinator)

        self._attr_name = "Phoniebox" + " " + config_entry.data[CONF_PHONIEBOX_NAME]
        self.entity_id = _slug(config_entry.data[CONF_PHONIEBOX_NAME])
        self._attr_state = None  # initially None to allow all attr to be initialised
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

    async def async_set_attributes(self, msg: ReceiveMessage) -> None:  # noqa: PLR0912
        """Set volume level."""
        changed_attribute_name = msg.topic.split("/")[2]
        new_value = str(msg.payload)

        if changed_attribute_name == PHONIEBOX_ATTR_VOLUME:
            self._attr_volume_level = float(new_value) / 100.0
        elif changed_attribute_name == PHONIEBOX_ATTR_STATE:
            self._attr_state = PHONIEBOX_STATE_TO_HA[new_value]
        elif changed_attribute_name == PHONIEBOX_ATTR_MUTE:
            self._attr_is_volume_muted = string_to_bool(new_value)
        elif changed_attribute_name == PHONIEBOX_ATTR_RANDOM:
            self._attr_shuffle = string_to_bool(new_value)
        elif changed_attribute_name == PHONIEBOX_ATTR_MAX_VOLUME:
            self._max_volume = int(new_value)
        elif changed_attribute_name == PHONIEBOX_ATTR_DURATION:
            self._attr_media_duration = sum(
                x * int(t)
                for x, t in zip([3600, 60, 1], new_value.split(":"), strict=False)
            )
        elif changed_attribute_name == PHONIEBOX_ATTR_TRACK:
            track_number = new_value.split(sep="/", maxsplit=1)[0]

            self._attr_media_track = int(track_number)
        elif changed_attribute_name == PHONIEBOX_ATTR_ELAPSED:
            self._attr_media_position = sum(
                x * int(t)
                for x, t in zip([3600, 60, 1], new_value.split(":"), strict=False)
            )
        elif changed_attribute_name == PHONIEBOX_ATTR_ARTIST:
            self._attr_media_artist = new_value
        elif changed_attribute_name == PHONIEBOX_ATTR_TITLE:
            self._attr_media_title = new_value
        elif changed_attribute_name == PHONIEBOX_ATTR_ALBUM:
            self._attr_media_album_name = new_value
        elif changed_attribute_name == PHONIEBOX_ATTR_ALBUM_ARTIST:
            self._attr_media_album_artist = new_value
        elif changed_attribute_name == PHONIEBOX_ATTR_VOLUME_STEPS:
            self._vol_steps = int(new_value)
        elif changed_attribute_name == PHONIEBOX_ATTR_REPEAT:
            if new_value == "true":
                # is bad but phoniebox will only say if repeat is on or off
                self._attr_repeat = REPEAT_MODE_ONE
            else:
                self._attr_repeat = REPEAT_MODE_OFF

        self.schedule_update_ha_state(force_refresh=True)

    async def update_device_state(self, msg: ReceiveMessage) -> None:
        """Update the device state."""
        before_state = self._attr_state
        if msg.payload == PHONIEBOX_STATE_OFFLINE:
            self._attr_state = MediaPlayerState.OFF
        elif self._attr_state in [
            MediaPlayerState.OFF,
            STATE_UNAVAILABLE,
            MEDIA_PLAYER_STATE_UNKNOWN,
            None,
        ]:
            self._attr_state = MediaPlayerState.IDLE

        if before_state != self._attr_state:
            self.schedule_update_ha_state(force_refresh=True)

    @override
    async def async_added_to_hass(self) -> None:
        """Subscribe to MQTT events."""
        LOGGER.info("media player added")
        await self.mqtt_client.async_subscribe("attribute/#", self.async_set_attributes)
        await self.mqtt_client.async_subscribe("state", self.update_device_state)

    @override
    async def async_volume_up(self) -> None:
        """Volume up the media player."""
        await self.mqtt_client.async_publish_cmd(PHONIEBOX_CMD_VOLUME_UP, None)

    @override
    async def async_volume_down(self) -> None:
        """Volume up the media player."""
        await self.mqtt_client.async_publish_cmd(PHONIEBOX_CMD_VOLUME_DOWN, None)

    @override
    async def async_mute_volume(self, mute: bool) -> None:
        """Send the media player the command for muting the volume."""
        await self.mqtt_client.async_publish_cmd(
            PHONIEBOX_CMD_MUTE, bool_to_string(mute)
        )

    @override
    async def async_media_play(self) -> None:
        """Send play command."""
        await self.mqtt_client.async_publish_cmd(PHONIEBOX_CMD_PLAYER_PLAY, None)

    @override
    async def async_media_pause(self) -> None:
        """Send pause command."""
        await self.mqtt_client.async_publish_cmd(PHONIEBOX_CMD_PLAYER_PAUSE, None)

    @override
    async def async_media_stop(self) -> None:
        """Send stop command."""
        await self.mqtt_client.async_publish_cmd(PHONIEBOX_CMD_PLAYER_STOP, None)

    @override
    async def async_media_previous_track(self) -> None:
        """Send previous track command."""
        await self.mqtt_client.async_publish_cmd(PHONIEBOX_CMD_PLAYER_PREV, None)

    @override
    async def async_media_next_track(self) -> None:
        """Send next track command."""
        await self.mqtt_client.async_publish_cmd(PHONIEBOX_CMD_PLAYER_NEXT, None)

    @override
    async def async_media_seek(self, position: float) -> None:
        """Send seek command."""
        await self.mqtt_client.async_publish_cmd(PHONIEBOX_CMD_PLAYER_SEEK, position)

    @override
    async def async_set_shuffle(self, shuffle: bool) -> None:
        """Enable/disable shuffle mode."""
        await self.mqtt_client.async_publish_cmd(
            PHONIEBOX_CMD_PLAYER_SHUFFLE, bool_to_string(shuffle)
        )

    @override
    async def async_set_repeat(self, repeat: str) -> None:
        """Set repeat mode."""
        await self.mqtt_client.async_publish_cmd(
            PHONIEBOX_CMD_PLAYER_REPEAT, HA_REPEAT_TO_PHONIEBOX[repeat]
        )

    @override
    async def async_turn_off(self) -> None:
        """Turn the media player off."""
        await self.mqtt_client.async_publish_cmd(PHONIEBOX_CMD_SHUTDOWN, None)

    @override
    async def async_set_volume_level(self, volume: float) -> None:
        """Set volume level, range 0..1."""
        await self.mqtt_client.async_publish_cmd(
            PHONIEBOX_CMD_SET_VOLUME, int(volume * 100)
        )

    async def async_set_volume_steps(self, volume_steps: int) -> None:
        """Set volume steps, range 0..100."""
        await self.mqtt_client.async_publish_cmd(
            PHONIEBOX_CMD_SET_VOLUME_STEPS, volume_steps
        )

    async def async_set_max_volume(self, max_volume: int) -> None:
        """Set max volume, range 0..100."""
        await self.mqtt_client.async_publish_cmd(
            PHONIEBOX_CMD_SET_MAX_VOLUME, max_volume
        )

    async def async_set_idle_shutdown_timer(self, time: int) -> None:
        """Set timer when box is idle to shut down after, in minutes, range 0..60."""
        await self.mqtt_client.async_publish_cmd(PHONIEBOX_CMD_SET_IDLE_TIME, time)

    async def async_set_shutdown_after(self, time: int) -> None:
        """Set timer to shut down the box, in minutes, range 0..60."""
        await self.mqtt_client.async_publish_cmd(PHONIEBOX_CMD_SHUTDOWN_AFTER, time)

    async def async_set_sleep_timer(self, time: int) -> None:
        """Set timer to pause the box, in minutes, range 0..60."""
        await self.mqtt_client.async_publish_cmd(PHONIEBOX_CMD_PLAYER_STOP_AFTER, time)

    async def async_toggle_rfid(self, is_started: bool) -> None:  # noqa: FBT001
        """Start or stop the rfid service."""
        await self.mqtt_client.async_publish_cmd(
            PHONIEBOX_CMD_SET_RFID, TO_PHONIEBOX_START_STOP[bool_to_string(is_started)]
        )

    async def async_toggle_gpio(self, is_started: bool) -> None:  # noqa: FBT001
        """Start or stop the gpio service."""
        await self.mqtt_client.async_publish_cmd(
            PHONIEBOX_CMD_SET_GPIO, TO_PHONIEBOX_START_STOP[bool_to_string(is_started)]
        )

    async def async_swipe_card(self, card_id: str) -> None:
        """Swipe a card id."""
        await self.mqtt_client.async_publish_cmd(PHONIEBOX_CMD_SWIPE_CARD, card_id)

    async def async_play_folder(self, folder_name: str) -> None:
        """Play a folder. Important needs folder name not path."""
        await self.mqtt_client.async_publish_cmd(PHONIEBOX_CMD_PLAY_FOLDER, folder_name)

    async def async_play_folder_recursive(self, folder_name: str) -> None:
        """Play a folder. Important needs folder name not path."""
        await self.mqtt_client.async_publish_cmd(
            PHONIEBOX_CMD_PLAY_FOLDER_RECURSIVE, folder_name
        )

    async def async_seek(self, seek_position: int) -> None:
        """Seek to position."""
        await self.mqtt_client.async_publish_cmd(
            PHONIEBOX_CMD_PLAYER_SEEK, seek_position
        )

    async def async_rewind(self) -> None:
        """Rewind command."""
        await self.mqtt_client.async_publish_cmd(PHONIEBOX_CMD_PLAYER_REWIND, None)

    async def async_replay(self) -> None:
        """Replay command."""
        await self.mqtt_client.async_publish_cmd(PHONIEBOX_CMD_PLAYER_REPLAY, None)

    async def async_scan(self) -> None:
        """Scan command."""
        await self.mqtt_client.async_publish_cmd(PHONIEBOX_CMD_SCAN, None)

    async def async_turn_off_silent(self) -> None:
        """Turn the media player off silently."""
        await self.mqtt_client.async_publish_cmd(PHONIEBOX_CMD_SHUTDOWN_SILENT, None)

    async def async_restart(self) -> None:
        """Restart the media player."""
        await self.mqtt_client.async_publish_cmd(PHONIEBOX_CMD_REBOOT, None)

    async def async_disable_wifi(self) -> None:
        """
        Disables Wi-Fi.

        Not sure if this should be activated
        """
        raise NotImplementedError
        # await self.mqtt_client.async_publish_cmd(
        # PHONIEBOX_CMD_DISABLE_WIFI,{})
