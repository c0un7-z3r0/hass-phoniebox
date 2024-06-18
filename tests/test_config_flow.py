"""Test phoniebox config flow."""

from collections.abc import Generator
from unittest.mock import patch

import pytest
from homeassistant import config_entries, data_entry_flow
from homeassistant.core import HomeAssistant

from custom_components.phoniebox.const import DOMAIN


# This fixture bypasses the actual setup of the integration
# since we only want to test the config flow. We test the
# actual functionality of the integration in other test modules.
@pytest.fixture(autouse=True)
def bypass_setup_fixture() -> Generator:
    """Prevent setup."""
    with (
        patch("custom_components.phoniebox.async_setup", return_value=True),
        patch(
            "custom_components.phoniebox.async_setup_entry",
            return_value=True,
        ),
    ):
        yield


# Here we simulate a successful config flow from the backend.
async def test_successful_config_flow(hass: HomeAssistant, config: dict) -> None:
    """Test a successful config flow."""
    # Initialize a config flow
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    # Check that the config flow shows the user form as the first step
    assert result["type"] == data_entry_flow.RESULT_TYPE_FORM
    assert result["step_id"] == "user"

    # If a user were to enter `test_box` for name of the box and `test_phoniebox`
    # for the base mqtt topic, it would result in this function call
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], user_input=config
    )

    # Check that the config flow is complete and a new entry is created with
    # the input data
    assert result["type"] == data_entry_flow.RESULT_TYPE_CREATE_ENTRY
    assert result["title"] == "test_box"
    assert result["data"] == config
    assert result["result"]
