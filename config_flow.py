import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_NAME, CONF_API_KEY
from homeassistant.core import callback
from homeassistant.helpers import config_validation as cv

from .const import DOMAIN

class MistralAIAPIConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            try:
                return self.async_create_entry(title=user_input[CONF_NAME], data=user_input)
            except Exception as e:
                _LOGGER.error(f"Error during configuration: {e}")
                errors["base"] = "unknown"

        data_schema = vol.Schema({
            vol.Required(CONF_NAME): cv.string,
            vol.Required(CONF_API_KEY): cv.string,
        })

        return self.async_show_form(
            step_id="user", data_schema=data_schema, errors=errors
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return MistralAIAPIOptionsFlowHandler(config_entry)

class MistralAIAPIOptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            self.hass.config_entries.async_update_entry(
                self.config_entry, data=user_input
            )
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Required(CONF_NAME, default=self.config_entry.data.get(CONF_NAME)): cv.string,
                vol.Required(CONF_API_KEY, default=self.config_entry.data.get(CONF_API_KEY)): cv.string,
            }),
        )
