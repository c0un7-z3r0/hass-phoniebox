"""Constants for phoniebox."""
from homeassistant.components.media_player.const import (
    REPEAT_MODE_ALL,
    REPEAT_MODE_OFF,
    REPEAT_MODE_ONE,
    SUPPORT_NEXT_TRACK,
    SUPPORT_PAUSE,
    SUPPORT_PLAY,
    SUPPORT_PREVIOUS_TRACK,
    SUPPORT_REPEAT_SET,
    SUPPORT_SEEK,
    SUPPORT_SHUFFLE_SET,
    SUPPORT_STOP,
    SUPPORT_TURN_OFF,
    SUPPORT_VOLUME_MUTE,
    SUPPORT_VOLUME_SET,
    SUPPORT_VOLUME_STEP,
)

# Base component constants
from homeassistant.const import (
    STATE_IDLE,
    STATE_PAUSED,
    STATE_PLAYING,
)

NAME = "Phoniebox"
DOMAIN = "phoniebox"
DOMAIN_DATA = f"{DOMAIN}_data"
VERSION = "0.3.0"
ATTRIBUTION = ""
ISSUE_URL = "https://github.com/c0un7-z3r0/hass-phoniebox/issues"

# Icons
ICON = "mdi:format-quote-close"

# Device classes
BINARY_SENSOR_DEVICE_CLASS = "connectivity"

# Custom Services
SERVICE_VOLUME_STEPS = "set_volume_steps"
SERVICE_MAX_VOLUME = "set_max_volume"
SERVICE_IDLE_TIMER = "set_idle_shutdown_timer"
SERVICE_SHUTDOWN_AFTER = "set_shutdown_after"
SERVICE_SLEEP_TIMER = "set_sleep_timer"
SERVICE_RFID = "set_rfid"
SERVICE_GPIO = "set_gpio"
SERVICE_SWIPE_CARD = "swipe_card"
SERVICE_PLAY_FOLDER = "play_folder"
SERVICE_PLAY_FOLDER_RECURSIVE = "play_folder_recursive"
SERVICE_PLAYER_SEEK = "player_seek"

SERVICE_REWIND = "player_rewind"
SERVICE_REPLAY = "player_replay"
SERVICE_SCAN = "scan"
SERVICE_TURN_OFF_SILENT = "silent_turn_off"
SERVICE_RESTART = "restart"
SERVICE_DISABLE_WIFI = "disable_wifi"

# Custom Attributes
ATTR_VOLUME_STEPS = "volume_steps"
ATTR_MAX_VOLUME = "max_volume"
ATTR_IDLE_TIME = "idle_time"
ATTR_IS_STARTED = "is_started"
ATTR_CARD_ID = "card_id"
ATTR_FOLDER_NAME = "folder_name"

# Platforms
BINARY_SENSOR = "binary_sensor"
SENSOR = "sensor"
SWITCH = "switch"
MEDIA_PLAYER = "media_player"
PLATFORMS = [SENSOR, BINARY_SENSOR, SWITCH, MEDIA_PLAYER]

# Player
SUPPORT_MQTTMEDIAPLAYER = (
        SUPPORT_PAUSE
        | SUPPORT_VOLUME_STEP
        | SUPPORT_PREVIOUS_TRACK
        | SUPPORT_VOLUME_SET
        | SUPPORT_NEXT_TRACK
        | SUPPORT_PLAY
        | SUPPORT_VOLUME_MUTE
        | SUPPORT_SHUFFLE_SET
        | SUPPORT_REPEAT_SET
        | SUPPORT_STOP
        | SUPPORT_SEEK
        | SUPPORT_TURN_OFF
)

PHONIEBOX_REPEAT_OFF = "off"
PHONIEBOX_REPEAT_SINGLE = "single"
PHONIEBOX_REPEAT_PLAYLIST = "playlist"

HA_REPEAT_TO_PHONIEBOX = {
    REPEAT_MODE_ONE: PHONIEBOX_REPEAT_SINGLE,
    REPEAT_MODE_OFF: PHONIEBOX_REPEAT_OFF,
    REPEAT_MODE_ALL: PHONIEBOX_REPEAT_PLAYLIST,
}

PHONIEBOX_START = "start"
PHONIEBOX_STOP = "stop"

TO_PHONIEBOX_START_STOP = {
    "true": PHONIEBOX_START,
    "false": PHONIEBOX_STOP
}

PHONIEBOX_STATE_PLAY = "play"
PHONIEBOX_STATE_STOP = "stop"
PHONIEBOX_STATE_PAUSE = "pause"

PHONIEBOX_STATE_TO_HA = {
    PHONIEBOX_STATE_PLAY: STATE_PLAYING,
    PHONIEBOX_STATE_STOP: STATE_IDLE,
    PHONIEBOX_STATE_PAUSE: STATE_PAUSED,
}

# Configuration and options
CONF_ENABLED = "enabled"
CONF_USERNAME = "username"
CONF_PASSWORD = "password"

CONF_PHONIEBOX_NAME = "phoniebox_name"
CONF_MQTT_BASE_TOPIC = "mqtt_base_topic"

# Defaults
DEFAULT_NAME = DOMAIN

BINARY_SWITCHES = [
    "gpio",
    "rfid",
    "random",
    "mute",
]
BOOLEAN_SENSORS = [
    "gpio",
    "rfid",
    "repeat",
    "random",
    "mute",
]
STRING_SENSORS = [
    "throttling",
    "version",
    "last_card",
    "album",
    "artist",
    "albumartist",
    "edition",
]
NUMBER_SENSORS = [
    "remaining_stopafter",
    "remaining_shutdownafter",
    "remaining_idle",
    "volstep",
    "maxvolume",
    "idletime",
]
GIGABYTE_SENSORS = [
    "disk_avail",
    "disk_total",
]
IGNORE_SENSORS = ["title", "track", "trackdate", "elapsed", "duration", "volume"]
