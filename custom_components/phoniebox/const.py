"""
Constants for the Phoniebox integration.

This module contains all constants, configuration keys, MQTT topics, commands,
and mappings used throughout the Phoniebox Home Assistant integration.
"""

from __future__ import annotations

from logging import Logger, getLogger
from typing import Final

from homeassistant.components.media_player.const import (
    MediaPlayerEntityFeature,
    MediaPlayerState,
    RepeatMode,
)
from homeassistant.const import Platform

LOGGER: Logger = getLogger(__package__)

# ===== BASIC INTEGRATION INFO =====
NAME: Final[str] = "Phoniebox"
DOMAIN: Final[str] = "phoniebox"
DOMAIN_DATA: Final[str] = f"{DOMAIN}_data"
VERSION: Final[str] = "0.8.0"  # Should match manifest.json
ATTRIBUTION: Final[str] = ""
ISSUE_URL: Final[str] = "https://github.com/c0un7-z3r0/hass-phoniebox/issues"

# ===== UI ELEMENTS =====
# Icons
ICON: Final[str] = "mdi:format-quote-close"

# Device classes
BINARY_SENSOR_DEVICE_CLASS: Final[str] = "connectivity"

# ===== PLATFORMS =====
BINARY_SENSOR: Final[str] = "binary_sensor"
SENSOR: Final[str] = "sensor"
SWITCH: Final[str] = "switch"
MEDIA_PLAYER: Final[str] = "media_player"
PLATFORMS: Final[list[Platform | str]] = [
    MEDIA_PLAYER,
    SENSOR,
    BINARY_SENSOR,
    SWITCH,
    Platform.BUTTON,
]

# ===== CUSTOM SERVICES =====
SERVICE_VOLUME_STEPS: Final[str] = "set_volume_steps"
SERVICE_MAX_VOLUME: Final[str] = "set_max_volume"
SERVICE_IDLE_TIMER: Final[str] = "set_idle_shutdown_timer"
SERVICE_SHUTDOWN_AFTER: Final[str] = "set_shutdown_after"
SERVICE_SLEEP_TIMER: Final[str] = "set_sleep_timer"
SERVICE_RFID: Final[str] = "set_rfid"
SERVICE_GPIO: Final[str] = "set_gpio"
SERVICE_SWIPE_CARD: Final[str] = "swipe_card"
SERVICE_PLAY_FOLDER: Final[str] = "play_folder"
SERVICE_PLAY_FOLDER_RECURSIVE: Final[str] = "play_folder_recursive"
SERVICE_PLAYER_SEEK: Final[str] = "player_seek"

SERVICE_REWIND: Final[str] = "player_rewind"
SERVICE_REPLAY: Final[str] = "player_replay"
SERVICE_SCAN: Final[str] = "scan"
SERVICE_TURN_OFF_SILENT: Final[str] = "silent_turn_off"
SERVICE_RESTART: Final[str] = "restart"
SERVICE_DISABLE_WIFI: Final[str] = "disable_wifi"

# Custom Attributes
ATTR_VOLUME_STEPS: Final[str] = "volume_steps"
ATTR_MAX_VOLUME: Final[str] = "max_volume"
ATTR_IDLE_TIME: Final[str] = "idle_time"
ATTR_IS_STARTED: Final[str] = "is_started"
ATTR_CARD_ID: Final[str] = "card_id"
ATTR_FOLDER_NAME: Final[str] = "folder_name"

# ===== MEDIA PLAYER CONFIGURATION =====
# Supported features for the MQTT media player
# noinspection SpellCheckingInspection
SUPPORT_MQTTMEDIAPLAYER: Final[MediaPlayerEntityFeature] = (
    MediaPlayerEntityFeature.PAUSE
    | MediaPlayerEntityFeature.VOLUME_STEP
    | MediaPlayerEntityFeature.PREVIOUS_TRACK
    | MediaPlayerEntityFeature.VOLUME_SET
    | MediaPlayerEntityFeature.NEXT_TRACK
    | MediaPlayerEntityFeature.PLAY
    | MediaPlayerEntityFeature.VOLUME_MUTE
    | MediaPlayerEntityFeature.SHUFFLE_SET
    | MediaPlayerEntityFeature.REPEAT_SET
    | MediaPlayerEntityFeature.STOP
    | MediaPlayerEntityFeature.SEEK
    | MediaPlayerEntityFeature.TURN_OFF
)

# ===== REPEAT MODE MAPPINGS =====
# Phoniebox repeat mode constants
PHONIEBOX_REPEAT_OFF: Final[str] = "off"
PHONIEBOX_REPEAT_SINGLE: Final[str] = "single"
PHONIEBOX_REPEAT_PLAYLIST: Final[str] = "playlist"

# Mapping from Home Assistant repeat modes to Phoniebox repeat modes
HA_REPEAT_TO_PHONIEBOX: Final[dict[RepeatMode, str]] = {
    RepeatMode.ONE: PHONIEBOX_REPEAT_SINGLE,
    RepeatMode.OFF: PHONIEBOX_REPEAT_OFF,
    RepeatMode.ALL: PHONIEBOX_REPEAT_PLAYLIST,
}

# ===== PLAYER STATE MAPPINGS =====
# Phoniebox player states
PHONIEBOX_START: Final[str] = "start"
PHONIEBOX_STOP: Final[str] = "stop"

# Boolean to start/stop command mapping
TO_PHONIEBOX_START_STOP: Final[dict[str, str]] = {
    "true": PHONIEBOX_START,
    "false": PHONIEBOX_STOP,
}

# Phoniebox state constants
PHONIEBOX_STATE_OFFLINE: Final[str] = "offline"
PHONIEBOX_STATE_PLAY: Final[str] = "play"
PHONIEBOX_STATE_STOP: Final[str] = "stop"
PHONIEBOX_STATE_PAUSE: Final[str] = "pause"

MEDIA_PLAYER_STATE_UNKNOWN: Final[str] = "unknown"

# Mapping from Phoniebox states to Home Assistant media player states
PHONIEBOX_STATE_TO_HA: Final[dict[str, MediaPlayerState]] = {
    "-": MediaPlayerState.OFF,
    PHONIEBOX_STATE_PLAY: MediaPlayerState.PLAYING,
    PHONIEBOX_STATE_STOP: MediaPlayerState.IDLE,
    PHONIEBOX_STATE_PAUSE: MediaPlayerState.PAUSED,
}

# ===== CONFIGURATION =====
# Configuration and options
CONF_ENABLED: Final[str] = "enabled"
CONF_USERNAME: Final[str] = "username"
CONF_PASSWORD: Final[str] = "password"

CONF_PHONIEBOX_NAME: Final[str] = "phoniebox_name"
CONF_MQTT_BASE_TOPIC: Final[str] = "mqtt_base_topic"

# Defaults
DEFAULT_NAME: Final[str] = DOMAIN

# ===== PHONIEBOX ATTRIBUTES =====
# Phoniebox device and state attributes
PHONIEBOX_ATTR_GPIO: Final[str] = "gpio"
PHONIEBOX_ATTR_RFID: Final[str] = "rfid"
PHONIEBOX_ATTR_MUTE: Final[str] = "mute"
PHONIEBOX_ATTR_RANDOM: Final[str] = "random"
PHONIEBOX_ATTR_SCAN: Final[str] = "scan"
# noinspection SpellCheckingInspection
PHONIEBOX_ATTR_PLAYER_REWIND: Final[str] = "playerrewind"
PHONIEBOX_ATTR_REPEAT: Final[str] = "repeat"
PHONIEBOX_ATTR_THROTTLING: Final[str] = "throttling"
PHONIEBOX_ATTR_VERSION: Final[str] = "version"
PHONIEBOX_ATTR_LAST_CARD: Final[str] = "last_card"

# Media attributes
PHONIEBOX_ATTR_ALBUM: Final[str] = "album"
PHONIEBOX_ATTR_ARTIST: Final[str] = "artist"
# noinspection SpellCheckingInspection
PHONIEBOX_ATTR_ALBUM_ARTIST: Final[str] = "albumartist"
PHONIEBOX_ATTR_EDITION: Final[str] = "edition"
PHONIEBOX_ATTR_TITLE: Final[str] = "title"
PHONIEBOX_ATTR_TRACK: Final[str] = "track"
# noinspection SpellCheckingInspection
PHONIEBOX_ATTR_TRACK_DATE: Final[str] = "trackdate"

# Timer and volume attributes
# noinspection SpellCheckingInspection
PHONIEBOX_ATTR_REMAINING_STOP_AFTER: Final[str] = "remaining_stopafter"
# noinspection SpellCheckingInspection
PHONIEBOX_ATTR_REMAINING_SHUTDOWN_AFTER: Final[str] = "remaining_shutdownafter"
PHONIEBOX_ATTR_REMAINING_IDLE: Final[str] = "remaining_idle"
# noinspection SpellCheckingInspection
PHONIEBOX_ATTR_VOLUME_STEPS: Final[str] = "volstep"
# noinspection SpellCheckingInspection
PHONIEBOX_ATTR_MAX_VOLUME: Final[str] = "maxvolume"
PHONIEBOX_ATTR_IDLE_TIME: Final[str] = "idletime"
PHONIEBOX_ATTR_VOLUME: Final[str] = "volume"

# Storage attributes
PHONIEBOX_ATTR_DISK_AVAILABLE: Final[str] = "disk_avail"
PHONIEBOX_ATTR_DISK_TOTAL: Final[str] = "disk_total"

# Playback attributes
PHONIEBOX_ATTR_ELAPSED: Final[str] = "elapsed"
PHONIEBOX_ATTR_DURATION: Final[str] = "duration"
PHONIEBOX_ATTR_STATE: Final[str] = "state"

# ===== PHONIEBOX COMMANDS =====
# Media player commands
# noinspection SpellCheckingInspection
PHONIEBOX_CMD_PLAYER_PLAY: Final[str] = "playerplay"
# noinspection SpellCheckingInspection
PHONIEBOX_CMD_PLAYER_PAUSE: Final[str] = "playerpause"
# noinspection SpellCheckingInspection
PHONIEBOX_CMD_PLAYER_STOP: Final[str] = "playerstop"
# noinspection SpellCheckingInspection
PHONIEBOX_CMD_PLAYER_NEXT: Final[str] = "playernext"
# noinspection SpellCheckingInspection
PHONIEBOX_CMD_PLAYER_PREV: Final[str] = "playerprev"
# noinspection SpellCheckingInspection
PHONIEBOX_CMD_PLAYER_SHUFFLE: Final[str] = "playershuffle"
# noinspection SpellCheckingInspection
PHONIEBOX_CMD_PLAYER_REPEAT: Final[str] = "playerrepeat"
# noinspection SpellCheckingInspection
PHONIEBOX_CMD_PLAYER_SEEK: Final[str] = "playerseek"
# noinspection SpellCheckingInspection
PHONIEBOX_CMD_PLAYER_REWIND: Final[str] = "playerrewind"
# noinspection SpellCheckingInspection
PHONIEBOX_CMD_PLAYER_REPLAY: Final[str] = "playerreplay"
# noinspection SpellCheckingInspection
PHONIEBOX_CMD_PLAYER_STOP_AFTER: Final[str] = "playerstopafter"

# Volume commands
# noinspection SpellCheckingInspection
PHONIEBOX_CMD_SET_VOLUME: Final[str] = "setvolume"
# noinspection SpellCheckingInspection
PHONIEBOX_CMD_VOLUME_UP: Final[str] = "volumeup"
# noinspection SpellCheckingInspection
PHONIEBOX_CMD_VOLUME_DOWN: Final[str] = "volumedown"
PHONIEBOX_CMD_MUTE: Final[str] = "mute"
# noinspection SpellCheckingInspection
PHONIEBOX_CMD_SET_VOLUME_STEPS: Final[str] = "setvolstep"
# noinspection SpellCheckingInspection
PHONIEBOX_CMD_SET_MAX_VOLUME: Final[str] = "setmaxvolume"

# Configuration commands
PHONIEBOX_CMD_SET_GPIO: Final[str] = "gpio"
PHONIEBOX_CMD_SET_RFID: Final[str] = "rfid"
# noinspection SpellCheckingInspection
PHONIEBOX_CMD_SET_IDLE_TIME: Final[str] = "setidletime"

# System commands
PHONIEBOX_CMD_SHUTDOWN: Final[str] = "shutdown"
# noinspection SpellCheckingInspection
PHONIEBOX_CMD_SHUTDOWN_AFTER: Final[str] = "shutdownafter"
# noinspection SpellCheckingInspection
PHONIEBOX_CMD_SHUTDOWN_SILENT: Final[str] = "shutdownsilent"
PHONIEBOX_CMD_REBOOT: Final[str] = "reboot"
# noinspection SpellCheckingInspection
PHONIEBOX_CMD_DISABLE_WIFI: Final[str] = "disablewifi"

# File and folder commands
# noinspection SpellCheckingInspection
PHONIEBOX_CMD_PLAY_FOLDER: Final[str] = "playfolder"
# noinspection SpellCheckingInspection
PHONIEBOX_CMD_PLAY_FOLDER_RECURSIVE: Final[str] = "playfolderrecursive"
# noinspection SpellCheckingInspection
PHONIEBOX_CMD_SWIPE_CARD: Final[str] = "swipecard"

# Utility commands
PHONIEBOX_CMD_SCAN: Final[str] = "scan"

# ===== SENSOR CATEGORIZATION =====
# Binary switches that can be toggled
BINARY_SWITCHES: Final[list[str]] = [
    PHONIEBOX_ATTR_GPIO,
    PHONIEBOX_ATTR_RFID,
    PHONIEBOX_ATTR_MUTE,
]

# Boolean sensor attributes
BOOLEAN_SENSORS: Final[list[str]] = [
    PHONIEBOX_ATTR_GPIO,
    PHONIEBOX_ATTR_RFID,
    PHONIEBOX_ATTR_REPEAT,
    PHONIEBOX_ATTR_RANDOM,
    PHONIEBOX_ATTR_MUTE,
]

# String sensor attributes
STRING_SENSORS: Final[list[str]] = [
    PHONIEBOX_ATTR_THROTTLING,
    PHONIEBOX_ATTR_VERSION,
    PHONIEBOX_ATTR_LAST_CARD,
    PHONIEBOX_ATTR_ALBUM,
    PHONIEBOX_ATTR_ARTIST,
    PHONIEBOX_ATTR_ALBUM_ARTIST,
    PHONIEBOX_ATTR_EDITION,
]

# Numeric sensor attributes
NUMBER_SENSORS: Final[list[str]] = [
    PHONIEBOX_ATTR_REMAINING_STOP_AFTER,
    PHONIEBOX_ATTR_REMAINING_SHUTDOWN_AFTER,
    PHONIEBOX_ATTR_REMAINING_IDLE,
    PHONIEBOX_ATTR_VOLUME_STEPS,
    PHONIEBOX_ATTR_MAX_VOLUME,
    PHONIEBOX_ATTR_IDLE_TIME,
]

# Disk usage sensors (in gigabytes)
GIGABYTE_SENSORS: Final[list[str]] = [
    PHONIEBOX_ATTR_DISK_AVAILABLE,
    PHONIEBOX_ATTR_DISK_TOTAL,
]

# Sensors to ignore (handled elsewhere, like media player)
IGNORE_SENSORS: Final[list[str]] = [
    PHONIEBOX_ATTR_TITLE,
    PHONIEBOX_ATTR_TRACK,
    PHONIEBOX_ATTR_TRACK_DATE,
    PHONIEBOX_ATTR_ELAPSED,
    PHONIEBOX_ATTR_DURATION,
    PHONIEBOX_ATTR_VOLUME,
]

# ===== BUTTONS =====
# Button entity names
BUTTON_SHUFFLE: Final[str] = "Shuffle"
BUTTON_SCAN: Final[str] = "Start Scan"
BUTTON_REWIND: Final[str] = "Rewind"
BUTTON_REPLAY: Final[str] = "Replay"
BUTTON_RESTART: Final[str] = "Restart Phoniebox"
BUTTON_SHUTDOWN: Final[str] = "Shutdown Phoniebox"
BUTTON_SHUTDOWN_SILENT: Final[str] = "Shutdown Phoniebox silently"

# All available buttons
ALL_BUTTONS: Final[list[str]] = [
    BUTTON_SCAN,
    BUTTON_REWIND,
    BUTTON_REPLAY,
    BUTTON_RESTART,
    BUTTON_SHUTDOWN,
    BUTTON_SHUFFLE,
    BUTTON_SHUTDOWN_SILENT,
]

# ===== MQTT TOPIC CONFIGURATION =====
# Topic length constants for parsing
TOPIC_LENGTH_PLAYER_STATE: Final[int] = 3
TOPIC_LENGTH_GENERIC_STATE: Final[int] = 2

# Topic domain constants
TOPIC_DOMAIN_STATE: Final[str] = "state"
# noinspection SpellCheckingInspection
TOPIC_DOMAIN_TEMPERATUR: Final[str] = "temperature"
TOPIC_DOMAIN_FILE: Final[str] = "file"
TOPIC_DOMAIN_VERSION: Final[str] = "version"
TOPIC_DOMAIN_RANDOM: Final[str] = "random"

# ===== COMMAND MAPPINGS =====
# Mapping from button names to MQTT commands
NAME_TO_MQTT_COMMAND: Final[dict[str, str]] = {
    BUTTON_SHUFFLE: PHONIEBOX_CMD_PLAYER_SHUFFLE,
    BUTTON_SCAN: PHONIEBOX_CMD_SCAN,
    BUTTON_REWIND: PHONIEBOX_CMD_PLAYER_REWIND,
    BUTTON_REPLAY: PHONIEBOX_CMD_PLAYER_REPLAY,
    BUTTON_RESTART: PHONIEBOX_CMD_REBOOT,
    BUTTON_SHUTDOWN: PHONIEBOX_CMD_SHUTDOWN,
    BUTTON_SHUTDOWN_SILENT: PHONIEBOX_CMD_SHUTDOWN_SILENT,
}

# ===== FINAL SENSOR LISTS =====
# Diagnostic sensors (for device diagnostics) - defined after all dependencies
DIAGNOSTIC_SENSORS: Final[list[str]] = [
    PHONIEBOX_ATTR_THROTTLING,
    PHONIEBOX_ATTR_VERSION,
    PHONIEBOX_ATTR_EDITION,
    TOPIC_DOMAIN_TEMPERATUR,
    *GIGABYTE_SENSORS,
]

# ===== CONSTANTS SUMMARY =====
"""
This module organizes constants into logical groups for better maintainability:

1. BASIC INTEGRATION INFO: Core integration metadata
2. PLATFORMS: Supported Home Assistant platforms
3. CUSTOM SERVICES: Service definitions for extended functionality
4. MEDIA PLAYER CONFIGURATION: Media player features and state mappings
5. CONFIGURATION: Config flow and options constants
6. PHONIEBOX ATTRIBUTES: All MQTT attributes from Phoniebox
7. PHONIEBOX COMMANDS: All MQTT commands to control Phoniebox
8. SENSOR CATEGORIZATION: Organized sensor types for entity creation
9. BUTTONS: Button entity definitions
10. MQTT TOPIC CONFIGURATION: Topic parsing and structure
11. COMMAND MAPPINGS: Button to command translations

Type hints are provided for all constants using Final[] for immutability.
Constants are grouped logically with clear section headers for navigation.
"""
