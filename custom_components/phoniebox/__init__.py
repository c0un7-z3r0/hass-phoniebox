"""
Custom integration to integrate Phoniebox with Home Assistant.

For more details about this integration, please refer to
https://github.com/c0un7-z3r0/hass-phoniebox
"""
import asyncio
import logging
from datetime import timedelta

import homeassistant.components.mqtt as mqtt
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import Config, HomeAssistant

from .const import CONF_MQTT_BASE_TOPIC, DOMAIN, PLATFORMS

SCAN_INTERVAL = timedelta(seconds=30)

DEPENDENCIES = ["mqtt"]

_LOGGER: logging.Logger = logging.getLogger(__package__)


class MqttClient:
    def __init__(self, hass, base_topic) -> None:
        self.base_topic = base_topic
        self.hass = hass

    async def async_subscribe(self, topic, msg_callback) -> None:
        full_topic = self.base_topic + "/" + topic
        await mqtt.async_subscribe(self.hass, full_topic, msg_callback)

    async def async_publish(self, topic, payload) -> None:
        full_topic = self.base_topic + "/" + topic
        await mqtt.async_publish(self.hass, full_topic, payload)


async def async_setup(hass: HomeAssistant, config: Config):
    """Set up this integration using YAML is not supported."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up this integration using UI."""
    if hass.data.get(DOMAIN) is None:
        hass.data.setdefault(DOMAIN, {})

    base_topic = entry.data.get(CONF_MQTT_BASE_TOPIC)
    mqtt_client = MqttClient(hass, base_topic)
    coordinator = DataCoordinator(mqtt_client)
    hass.data[DOMAIN][entry.entry_id] = coordinator

    for platform in PLATFORMS:
        if entry.options.get(platform, True):
            coordinator.platforms.append(platform)
            hass.async_add_job(
                hass.config_entries.async_forward_entry_setup(entry, platform)
            )

    entry.add_update_listener(async_reload_entry)
    return True


class DataCoordinator:
    """Class to manage fetching data from the API."""

    def __init__(self, mqtt_client: MqttClient) -> None:
        """Initialize."""
        self.platforms = []
        self.mqtt_client = mqtt_client
        self.sensors = {}
        self.switches = {}
        self.version = "unknown"


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Handle removal of an entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    unloaded = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, platform)
                for platform in PLATFORMS
                if platform in coordinator.platforms
            ]
        )
    )
    if unloaded:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unloaded


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
