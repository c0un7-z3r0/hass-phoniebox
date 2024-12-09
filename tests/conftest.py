"""Global fixtures for phoniebox integration."""

from collections.abc import AsyncGenerator, Generator
from typing import Any

# Fixtures allow you to replace functions with a Mock object. You can perform
# many options via the Mock to reflect a particular behavior from the original
# function that you want to see without going through the function's actual logic.
# Fixtures can either be passed into tests as parameters, or if autouse=True, they
# will automatically be used across all tests.
#
# Fixtures that are defined in conftest.py are available across all tests. You can also
# define fixtures within a particular test file to scope them locally.
#
# pytest_homeassistant_custom_component provides some fixtures that are provided by
# Home Assistant core. You can find those fixture definitions here:
# https://github.com/MatthewFlamm/pytest-homeassistant-custom-component/blob/master/pytest_homeassistant_custom_component/common.py
#
# See here for more info: https://docs.pytest.org/en/latest/fixture.html (note that
# pytest includes fixtures OOB which you can use as defined on this page)
from unittest.mock import MagicMock, patch

import pytest
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry
from homeassistant.helpers.entity_registry import RegistryEntry
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.phoniebox.const import CONF_PHONIEBOX_NAME, DOMAIN

from .const import MOCK_CONFIG

pytest_plugins = "pytest_homeassistant_custom_component"


@pytest.fixture(name="config")
def config_fixture() -> dict:
    """Create hass config fixture."""
    return MOCK_CONFIG


@pytest.fixture(autouse=True)
async def p_mqtt_mock(mqtt_mock: MagicMock) -> MagicMock:
    """Fixture to mock MQTT component."""
    return mqtt_mock


@pytest.fixture
def mock_config_entry() -> MockConfigEntry:
    """Return the default mocked config entry."""
    return MockConfigEntry(
        title="Phoniebox Test",
        domain=DOMAIN,
        data=MOCK_CONFIG,
        entry_id=MOCK_CONFIG[CONF_PHONIEBOX_NAME],
        unique_id="Phoniebox-UUID",
    )


# This fixture enables loading custom integrations in all tests.
# Remove to enable selective use of this fixture
@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(enable_custom_integrations: Any) -> None:
    """Auto enable custom integration."""
    return


# This fixture is used to prevent HomeAssistant from attempting to create and
# dismiss persistent notifications. These calls would fail without this
# fixture since the persistent_notification
# integration is never loaded during a test.
@pytest.fixture(name="skip_notifications", autouse=True)
def skip_notifications_fixture() -> Generator:
    """Skip notification calls."""
    with (
        patch("homeassistant.components.persistent_notification.async_create"),
        patch("homeassistant.components.persistent_notification.async_dismiss"),
    ):
        yield


@pytest.fixture
async def mock_phoniebox(
    hass: HomeAssistant, mock_config_entry: MockConfigEntry
) -> MockConfigEntry:
    """Set up the Phoniebox integration in Home Assistant."""
    mock_config_entry.add_to_hass(hass)

    assert await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()
    return mock_config_entry


@pytest.fixture(name="media_player_entry")
def media_player_entry(hass: HomeAssistant) -> RegistryEntry | None:
    """Create hass config fixture."""
    er = entity_registry.async_get(hass)
    entry: RegistryEntry | None = er.async_get("media_player.phoniebox_test_box")
    return entry


@pytest.fixture(autouse=True)
async def cleanup_timers(hass: HomeAssistant) -> AsyncGenerator[None, None]:
    """Cancel all lingering timers."""
    yield
    # ruff: noqa: SLF001
    for timer in list(hass.loop._scheduled):
        timer.cancel()
