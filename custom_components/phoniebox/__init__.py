"""
Custom integration to integrate Phoniebox with Home Assistant.

For more details about this integration, please refer to
https://github.com/c0un7-z3r0/hass-phoniebox
"""

from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

from homeassistant.exceptions import ConfigEntryNotReady

from .const import CONF_MQTT_BASE_TOPIC, DOMAIN, LOGGER, PLATFORMS
from .data_coordinator import DataCoordinator
from .mqtt_client import MqttClient

if TYPE_CHECKING:
    from collections.abc import Sequence

    from homeassistant.config_entries import ConfigEntry
    from homeassistant.core import HomeAssistant


ERROR_MISSING_MQTT_TOPIC = "MQTT base topic is required but not configured"
ERROR_MQTT_CLIENT_INIT = "Failed to initialize MQTT client"
ERROR_PLATFORM_SETUP = "Failed to set up platforms"


async def async_setup(hass: HomeAssistant, config: dict) -> bool:  # noqa: ARG001
    """
    Set up this integration using YAML is not supported.

    Args:
    ----
        hass: The Home Assistant instance
        config: The configuration dictionary from configuration.yaml

    Returns:
    -------
        True if setup is successful, False otherwise

    Note:
    ----
        This integration only supports configuration through the UI.
        YAML configuration is not supported.

    """
    LOGGER.info("Phoniebox integration setup called (YAML not supported)")
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """
    Set up Phoniebox integration from a config entry.

    This function initializes the MQTT client, data coordinator, and sets up
    all enabled platforms for the Phoniebox integration.

    Args:
    ----
        hass: The Home Assistant instance
        entry: The config entry containing user configuration

    Returns:
    -------
        True if setup is successful

    Raises:
    ------
        ConfigEntryNotReady: If MQTT client initialization fails
        ValueError: If required configuration is missing

    """
    LOGGER.info("Setting up Phoniebox integration for entry: %s", entry.entry_id)

    # Initialize domain data if not exists
    hass.data.setdefault(DOMAIN, {})

    # Validate required configuration
    base_topic = entry.data.get(CONF_MQTT_BASE_TOPIC)
    if not base_topic:
        LOGGER.error(ERROR_MISSING_MQTT_TOPIC)
        raise ValueError(ERROR_MISSING_MQTT_TOPIC)

    # Initialize MQTT client and coordinator
    try:
        LOGGER.debug("Initializing MQTT client with base topic: %s", base_topic)
        mqtt = MqttClient(hass, str(base_topic))
        coordinator = DataCoordinator(mqtt)
        hass.data[DOMAIN][entry.entry_id] = coordinator
    except Exception as err:
        LOGGER.error("%s: %s", ERROR_MQTT_CLIENT_INIT, err)
        msg = f"{ERROR_MQTT_CLIENT_INIT}: {err}"
        raise ConfigEntryNotReady(msg) from err

    # Collect enabled platforms using functional approach
    enabled_platforms: list[str] = _get_enabled_platforms(entry, PLATFORMS)

    # Store enabled platforms in coordinator
    coordinator.platforms = enabled_platforms.copy()

    LOGGER.info("Enabled platforms: %s", enabled_platforms)

    # Setup platforms if any are enabled
    if enabled_platforms:
        try:
            await hass.config_entries.async_forward_entry_setups(
                entry, enabled_platforms
            )
            LOGGER.info("Successfully set up %d platforms", len(enabled_platforms))
        except Exception as err:
            LOGGER.error("Failed to set up platforms: %s", err)
            msg = f"Failed to set up platforms: {err}"
            raise ConfigEntryNotReady(msg) from err

    # Register update listener for config changes
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    LOGGER.info("Phoniebox integration setup completed successfully")
    return True


def _get_enabled_platforms(
    entry: ConfigEntry, available_platforms: Sequence[str]
) -> list[str]:
    """
    Get list of enabled platforms from config entry options.

    Args:
    ----
        entry: The config entry containing platform options
        available_platforms: List of all available platform names

    Returns:
    -------
        List of enabled platform names

    Note:
    ----
        Platforms are enabled by default if not explicitly disabled in options.

    """
    return [
        platform for platform in available_platforms
        if entry.options.get(platform, True)
    ]


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """
    Handle removal of a config entry.

    Unloads all platforms associated with the entry and cleans up resources.

    Args:
    ----
        hass: The Home Assistant instance
        entry: The config entry to unload

    Returns:
    -------
        True if unload is successful, False otherwise

    Note:
    ----
        This function is graceful and will return True even if the entry
        was already removed or never existed.

    """
    LOGGER.info("Unloading Phoniebox integration for entry: %s", entry.entry_id)

    try:
        coordinator = hass.data[DOMAIN][entry.entry_id]

        # Unload all platforms that were set up
        unload_tasks = [
            hass.config_entries.async_forward_entry_unload(entry, platform)
            for platform in coordinator.platforms
        ]

        if unload_tasks:
            LOGGER.debug("Unloading %d platforms", len(unload_tasks))
            unloaded = all(await asyncio.gather(*unload_tasks, return_exceptions=False))
        else:
            LOGGER.debug("No platforms to unload")
            unloaded = True

        if unloaded:
            hass.data[DOMAIN].pop(entry.entry_id)
            LOGGER.info("Successfully unloaded Phoniebox integration")
            return True
        LOGGER.warning("Some platforms failed to unload properly")
        return False  # noqa: TRY300
    except KeyError:
        # Entry was already removed or never existed
        LOGGER.debug("Entry %s was already removed or never existed", entry.entry_id)
        return True
    except (ValueError, TypeError, RuntimeError) as err:
        LOGGER.error("Unexpected error during unload: %s", err)
        return False


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """
    Reload a config entry.

    This function performs a complete reload by first unloading the entry
    and then setting it up again with the current configuration.

    Args:
    ----
        hass: The Home Assistant instance
        entry: The config entry to reload

    Note:
    ----
        This function is typically called when the user updates the
        integration configuration through the UI.

    """
    LOGGER.info("Reloading Phoniebox integration for entry: %s", entry.entry_id)

    try:
        await async_unload_entry(hass, entry)
        await async_setup_entry(hass, entry)
        LOGGER.info("Successfully reloaded Phoniebox integration")
    except Exception as err:
        LOGGER.error("Failed to reload integration: %s", err)
        raise
