"""Test integration_blueprint setup process."""

from custom_components.phoniebox import (
    DataCoordinator,
    MqttClient,
    async_reload_entry,
    async_setup_entry,
    async_unload_entry,
)
from custom_components.phoniebox.const import DOMAIN, MEDIA_PLAYER


# We can pass fixtures as defined in conftest.py to tell pytest to use the fixture
# for a given test. We can also leverage fixtures and mocks that are available in
# Home Assistant using the pytest_homeassistant_custom_component plugin.
# Assertions allow you to verify that the return value of whatever is on the left
# side of the assertion matches with the right side.
async def test_setup_unload_and_reload_entry(hass, mock_phoniebox):
    """Test entry setup and unload."""

    config_entry = mock_phoniebox
    # Set up the entry and assert that the values set during setup are where we expect
    assert await async_setup_entry(hass, config_entry)
    assert DOMAIN in hass.data and config_entry.entry_id in hass.data[DOMAIN]
    assert type(hass.data[DOMAIN][config_entry.entry_id]) == DataCoordinator
    assert MEDIA_PLAYER in hass.data[DOMAIN][config_entry.entry_id].platforms
    assert type(hass.data[DOMAIN][config_entry.entry_id].mqtt_client) == MqttClient

    assert hass.services

    # Reload the entry and assert that the data from above is still there
    assert await async_reload_entry(hass, config_entry) is None
    assert DOMAIN in hass.data and config_entry.entry_id in hass.data[DOMAIN]
    assert type(hass.data[DOMAIN][config_entry.entry_id]) == DataCoordinator
    assert MEDIA_PLAYER in hass.data[DOMAIN][config_entry.entry_id].platforms
    assert type(hass.data[DOMAIN][config_entry.entry_id].mqtt_client) == MqttClient

    # Unload the entry and verify that the data has been removed
    assert await async_unload_entry(hass, config_entry)
    assert config_entry.entry_id not in hass.data[DOMAIN]
