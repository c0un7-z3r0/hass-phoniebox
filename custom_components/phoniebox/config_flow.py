# mypy: disable-error-code="no-any-return"
"""Adds config flow for Blueprint."""

from typing import Any, override

import voluptuous as vol
from homeassistant import config_entries

from .const import CONF_MQTT_BASE_TOPIC, CONF_PHONIEBOX_NAME, DOMAIN


class BlueprintFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Blueprint."""

    VERSION = 1

    _errors: dict[str, str]

    def __init__(self) -> None:
        """Initialize."""
        self._errors = {}

    @override
    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.ConfigFlowResult:
        """Handle a flow initialized by the user."""
        self._errors = {}

        if user_input is not None:
            if user_input[CONF_PHONIEBOX_NAME] and user_input[CONF_MQTT_BASE_TOPIC]:
                return self.async_create_entry(
                    title=user_input[CONF_PHONIEBOX_NAME], data=user_input
                )
            self._errors["base"] = "auth"

            return self._show_config_form(user_input)

        # Provide defaults for form
        user_input = {CONF_PHONIEBOX_NAME: "", CONF_MQTT_BASE_TOPIC: "phoniebox"}

        return self._show_config_form(user_input)

    def _show_config_form(
        self, user_input: dict[str, str]
    ) -> config_entries.ConfigFlowResult:
        """Show the configuration form to edit location data."""
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_PHONIEBOX_NAME, default=user_input[CONF_PHONIEBOX_NAME]
                    ): str,
                    vol.Required(
                        CONF_MQTT_BASE_TOPIC, default=user_input[CONF_MQTT_BASE_TOPIC]
                    ): str,
                }
            ),
            errors=self._errors,
        )
