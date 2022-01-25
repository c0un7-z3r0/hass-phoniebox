"""Constants for integration_blueprint."""
from homeassistant.components.media_player.const import (
    SUPPORT_NEXT_TRACK,
    SUPPORT_PAUSE,
    SUPPORT_PLAY,
    SUPPORT_PREVIOUS_TRACK,
    SUPPORT_VOLUME_SET,
    SUPPORT_VOLUME_STEP,
    SUPPORT_VOLUME_MUTE,
    SUPPORT_SHUFFLE_SET, SUPPORT_CLEAR_PLAYLIST, SUPPORT_GROUPING, SUPPORT_PLAY_MEDIA, SUPPORT_REPEAT_SET, SUPPORT_SEEK,
    SUPPORT_SELECT_SOURCE, SUPPORT_STOP,
)

# Base component constants
from homeassistant.const import STATE_PLAYING, STATE_IDLE, STATE_PAUSED

NAME = "Phoniebox"
DOMAIN = "phoniebox"
DOMAIN_DATA = f"{DOMAIN}_data"
VERSION = "0.0.1"
ATTRIBUTION = ""
ISSUE_URL = "https://github.com/c0un7-z3r0/hass-phoniebox/issues"

# Icons
ICON = "mdi:format-quote-close"

# Device classes
BINARY_SENSOR_DEVICE_CLASS = "connectivity"

# Platforms
BINARY_SENSOR = "binary_sensor"
SENSOR = "sensor"
SWITCH = "switch"
MEDIA_PLAYER = "media_player"
PLATFORMS = [SENSOR, BINARY_SENSOR,SWITCH, MEDIA_PLAYER]

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
)


PHONIEBOX_STATE_PLAY = "play"
PHONIEBOX_STATE_STOP = "stop"
PHONIEBOX_STATE_PAUSE = "pause"

PHONIEBOX_STATE_TO_HA = {
    PHONIEBOX_STATE_PLAY: STATE_PLAYING,
    PHONIEBOX_STATE_STOP: STATE_IDLE,
    PHONIEBOX_STATE_PAUSE: STATE_PAUSED
}

# Configuration and options
CONF_ENABLED = "enabled"
CONF_USERNAME = "username"
CONF_PASSWORD = "password"

CONF_PHONIEBOX_NAME = "phoniebox_name"
CONF_MQTT_BASE_TOPIC = "mqtt_base_topic"

# Defaults
DEFAULT_NAME = DOMAIN

BINARY_SWITCHES = ["gpio", "rfid", "random", "mute", ]
BOOLEAN_SENSORS = ["gpio", "rfid", "repeat", "random", "mute", ]
STRING_SENSORS = ["throttling", "version", "last_card", "album", "artist", "albumartist", "edition"]
NUMBER_SENSORS = ["remaining_stopafter", "remaining_shutdownafter", "remaining_idle", "volstep", "maxvolume",
                  "idletime"]
GIGABYTE_SENSORS = ["disk_avail", "disk_total", ]
IGNORE_SENSORS = ["title", "track", "trackdate", "elapsed", "duration", "volume"]
