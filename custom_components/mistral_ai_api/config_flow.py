# home_assistant_mistral_ai/config_flow.py

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from .const import DOMAIN

class MistralAIConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Mistral AI."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_PUSH

    def __init__(self):
        """Initialize the config flow."""
        pass

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            return self.async_create_entry(title="Mistral AI", data=user_input)

        data_schema = vol.Schema({
            vol.Required("api_key"): str,
        })

        return self.async_show_form(
            step_id="user", data_schema=data_schema, errors=errors
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return MistralAIOptionsFlowHandler(config_entry)

class MistralAIOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle an options flow for Mistral AI."""

    def __init__(self, config_entry):
        """Initialize Mistral AI options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        return await self.async_step_user()

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        options_schema = vol.Schema({
            vol.Required("api_key", default=self.config_entry.options.get("api_key", "")): str,
        })

        return self.async_show_form(
            step_id="user", data_schema=options_schema
        )
