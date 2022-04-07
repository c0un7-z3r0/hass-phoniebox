"""Constants for phoniebox."""
from logging import Logger, getLogger
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
    STATE_PLAYING, Platform,
)

LOGGER: Logger = getLogger(__package__)

NAME = "Phoniebox"
DOMAIN = "phoniebox"
DOMAIN_DATA = f"{DOMAIN}_data"
VERSION = "0.3.1"
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
PLATFORMS = [SENSOR, BINARY_SENSOR, SWITCH, MEDIA_PLAYER, Platform.BUTTON]

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

# Phoniebox attributes
PHONIEBOX_ATTR_GPIO = "gpio"
PHONIEBOX_ATTR_RFID = "rfid"
PHONIEBOX_ATTR_MUTE = "mute"
PHONIEBOX_ATTR_RANDOM = "random"
PHONIEBOX_ATTR_SCAN = "scan"
PHONIEBOX_ATTR_PLAYER_REWIND = "playerrewind"
PHONIEBOX_ATTR_REPEAT = "repeat"
PHONIEBOX_ATTR_THROTTLING = "throttling"
PHONIEBOX_ATTR_VERSION = "version"
PHONIEBOX_ATTR_LAST_CARD = "last_card"
PHONIEBOX_ATTR_ALBUM = "album"
PHONIEBOX_ATTR_ARTIST = "artist"
PHONIEBOX_ATTR_ALBUM_ARTIST = "albumartist"
PHONIEBOX_ATTR_EDITION = "edition"
PHONIEBOX_ATTR_REMAINING_STOP_AFTER = "remaining_stopafter"
PHONIEBOX_ATTR_REMAINING_SHUTDOWN_AFTER = "remaining_shutdownafter"
PHONIEBOX_ATTR_REMAINING_IDLE = "remaining_idle"
PHONIEBOX_ATTR_VOLUME_STEPS = "volstep"
PHONIEBOX_ATTR_MAX_VOLUME = "maxvolume"
PHONIEBOX_ATTR_IDLE_TIME = "idletime"
PHONIEBOX_ATTR_DISK_AVAILABLE = "disk_avail"
PHONIEBOX_ATTR_DISK_TOTAL = "disk_total"
PHONIEBOX_ATTR_TITLE = "title"
PHONIEBOX_ATTR_TRACK = "track"
PHONIEBOX_ATTR_TRACK_DATE = "trackdate"
PHONIEBOX_ATTR_ELAPSED = "elapsed"
PHONIEBOX_ATTR_DURATION = "duration"
PHONIEBOX_ATTR_VOLUME = "volume"

# Phoniebox commands
PHONIEBOX_CMD_DISABLE_WIFI = "disablewifi"
PHONIEBOX_CMD_SCAN = "scan"
PHONIEBOX_CMD_REBOOT = "reboot"
PHONIEBOX_CMD_SHUTDOWN_SILENT = "shutdownsilent"
PHONIEBOX_CMD_PLAYER_REPLAY = "playerreplay"
PHONIEBOX_CMD_PLAYER_REWIND = "playerrewind"
PHONIEBOX_CMD_PLAYER_SEEK = "playerseek"
PHONIEBOX_CMD_PLAY_FOLDER_RECURSIVE = "playfolderrecursive"
PHONIEBOX_CMD_PLAY_FOLDER = "playfolder"
PHONIEBOX_CMD_SWIPE_CARD = "swipecard"
PHONIEBOX_CMD_SET_GPIO = "gpio"
PHONIEBOX_CMD_SET_RFID = "rfid"
PHONIEBOX_CMD_PLAYER_STOP_AFTER = "playerstopafter"
PHONIEBOX_CMD_SHUTDOWN_AFTER = "shutdownafter"
PHONIEBOX_CMD_SET_IDLE_TIME = "setidletime"
PHONIEBOX_CMD_SET_MAX_VOLUME = "setmaxvolume"
PHONIEBOX_CMD_SET_VOLUME_STEPS = "setvolstep"
PHONIEBOX_CMD_SET_VOLUME = "setvolume"
PHONIEBOX_CMD_SHUTDOWN = "shutdown"
PHONIEBOX_CMD_PLAYER_REPEAT = "playerrepeat"
PHONIEBOX_CMD_PLAYER_SHUFFLE = "playershuffle"
PHONIEBOX_CMD_PLAYER_NEXT = "playernext"
PHONIEBOX_CMD_PLAYER_PREV = "playerprev"
PHONIEBOX_CMD_PLAYER_STOP = "playerstop"
PHONIEBOX_CMD_PLAYER_PAUSE = "playerpause"
PHONIEBOX_CMD_PLAYER_PLAY = "playerplay"
PHONIEBOX_CMD_MUTE = "mute"
PHONIEBOX_CMD_VOLUME_DOWN = "volumedown"
PHONIEBOX_CMD_VOLUME_UP = "volumeup"

BINARY_SWITCHES = [
    PHONIEBOX_ATTR_GPIO,
    PHONIEBOX_ATTR_RFID,
    PHONIEBOX_ATTR_MUTE,
]
BOOLEAN_SENSORS = [
    PHONIEBOX_ATTR_GPIO,
    PHONIEBOX_ATTR_RFID,
    PHONIEBOX_ATTR_REPEAT,
    PHONIEBOX_ATTR_RANDOM,
    PHONIEBOX_ATTR_MUTE,
]
STRING_SENSORS = [
    PHONIEBOX_ATTR_THROTTLING,
    PHONIEBOX_ATTR_VERSION,
    PHONIEBOX_ATTR_LAST_CARD,
    PHONIEBOX_ATTR_ALBUM,
    PHONIEBOX_ATTR_ARTIST,
    PHONIEBOX_ATTR_ALBUM_ARTIST,
    PHONIEBOX_ATTR_EDITION
]
NUMBER_SENSORS = [
    PHONIEBOX_ATTR_REMAINING_STOP_AFTER,
    PHONIEBOX_ATTR_REMAINING_SHUTDOWN_AFTER,
    PHONIEBOX_ATTR_REMAINING_IDLE,
    PHONIEBOX_ATTR_VOLUME_STEPS,
    PHONIEBOX_ATTR_MAX_VOLUME,
    PHONIEBOX_ATTR_IDLE_TIME,
]
GIGABYTE_SENSORS = [
    PHONIEBOX_ATTR_DISK_AVAILABLE,
    PHONIEBOX_ATTR_DISK_TOTAL,
]
IGNORE_SENSORS = [
    PHONIEBOX_ATTR_TITLE,
    PHONIEBOX_ATTR_TRACK,
    PHONIEBOX_ATTR_TRACK_DATE,
    PHONIEBOX_ATTR_ELAPSED,
    PHONIEBOX_ATTR_DURATION,
    PHONIEBOX_ATTR_VOLUME,
]

# Buttons
BUTTON_SHUFFLE = "Shuffle"
BUTTON_SCAN = "Start Scan"
BUTTON_REWIND = "Rewind"
BUTTON_REPLAY = "Replay"
BUTTON_RESTART = "Restart Phoniebox"
BUTTON_SHUTDOWN = "Shutdown Phoniebox"
BUTTON_SHUTDOWN_SILENT = "Shutdown Phoniebox silently"

ALL_BUTTONS = [
    BUTTON_SCAN,
    BUTTON_REWIND,
    BUTTON_REPLAY,
    BUTTON_RESTART,
    BUTTON_SHUTDOWN,
    BUTTON_SHUFFLE,
    BUTTON_SHUTDOWN_SILENT,
]
