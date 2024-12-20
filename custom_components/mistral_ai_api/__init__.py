import logging
import requests
from datetime import datetime
import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from homeassistant.const import CONF_NAME, CONF_API_KEY
from homeassistant.core import HomeAssistant
import asyncio
from homeassistant.config_entries import ConfigEntry
from .api import send_prompt_command

_LOGGER = logging.getLogger(__name__)

DOMAIN = "mistral_ai_api"

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Required(CONF_NAME): cv.string,
        vol.Required(CONF_API_KEY): cv.string
    }),
}, extra=vol.ALLOW_EXTRA)

async def async_setup(hass: HomeAssistant, config: dict):
    hass.data.setdefault(DOMAIN, {})

    if DOMAIN not in config:
        return True

    conf = config[DOMAIN]
    return await setup_common(hass, conf)

async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    conf = config_entry.data
    return await setup_common(hass, conf)

async def setup_common(hass: HomeAssistant, conf: dict) -> bool:
    api_key = conf[CONF_API_KEY]

    async def send_prompt(call):

        _LOGGER.debug(f"send_prompt {call}")
        prompt = call.data.get("prompt")
        agent_id = call.data.get("agent_id")
        identifier = call.data.get("identifier")
        model = call.data.get("model")
        timeout_in_seconds = call.data.get("timeout_in_seconds")

        await send_prompt_command(hass, api_key, prompt, agent_id, identifier, model, timeout_in_seconds)
        
    hass.services.async_register(DOMAIN, "send_prompt", send_prompt)
    return True

async def async_unload_entry(hass, entry):
    hass.services.async_remove(DOMAIN, "send_prompt")
    return True