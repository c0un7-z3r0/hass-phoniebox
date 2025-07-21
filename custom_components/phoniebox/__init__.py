"""
Custom integration to integrate Phoniebox with Home Assistant.

For more details about this integration, please refer to
https://github.com/c0un7-z3r0/hass-phoniebox
"""

import asyncio

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import Config, HomeAssistant, callback

from .const import CONF_MQTT_BASE_TOPIC, DOMAIN, PLATFORMS
from .data_coordinator import DataCoordinator
from .mqtt_client import MqttClient


async def async_setup(_hass: HomeAssistant, _config: Config) -> bool:
    """Set up this integration using YAML is not supported."""
    return True


@callback
async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up this integration using UI."""
    if hass.data.get(DOMAIN) is None:
        hass.data.setdefault(DOMAIN, {})

    base_topic = str(entry.data.get(CONF_MQTT_BASE_TOPIC))
    mqtt = MqttClient(hass, base_topic)
    coordinator = DataCoordinator(mqtt)
    hass.data[DOMAIN][entry.entry_id] = coordinator

    for platform in PLATFORMS:
        if entry.options.get(platform, True):
            coordinator.platforms.append(platform)
            await hass.config_entries.async_forward_entry_setups(
              entry, coordinator.platforms
            )

    entry.async_on_unload(entry.add_update_listener(async_reload_entry))
    return True


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
