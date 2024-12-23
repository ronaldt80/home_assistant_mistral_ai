import logging
import voluptuous as vol

from homeassistant.const import CONF_API_KEY, CONF_NAME
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.typing import ConfigType

import homeassistant.helpers.config_validation as cv

from .api import send_prompt_command
from .const import (
    ATTR_IDENTIFIER,
    ATTR_LAST_PROMPT,
    ATTR_LAST_RESPONSE,
    ATTR_TIMESTAMP,
    DOMAIN,
)
from .sensor import MistralAiSensor

_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {vol.Required(CONF_NAME): cv.string, vol.Required(CONF_API_KEY): cv.string}
        ),
    },
    extra=vol.ALLOW_EXTRA,
)
async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the Mistral AI component."""
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Mistral AI from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = entry.data
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    hass.data[DOMAIN].pop(entry.entry_id)
    return True

async def async_setup(hass: HomeAssistant, config: dict):
    hass.data.setdefault(DOMAIN, {})

    # Exclude attributes from being recorded in history
    _entity_component_unrecorded_attributes = frozenset(
        (ATTR_TIMESTAMP, ATTR_LAST_PROMPT, ATTR_LAST_RESPONSE, ATTR_IDENTIFIER)
    )

    # Initialize MistralAiSensor
    sensor = MistralAiSensor(
        hass, {"state": "idle", "response": "", "prompt": "", "identifier": ""}
    )
    sensor.async_write_ha_state()

    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(config, "sensor")
    )

    hass.data[DOMAIN]["sensor"] = sensor

    if DOMAIN not in config:
        return True

    conf = config[DOMAIN]
    return await setup_common(hass, conf)


async def setup_common(hass: HomeAssistant, conf: dict) -> bool:
    api_key = conf[CONF_API_KEY]

    async def send_prompt(call):
        prompt = call.data.get("prompt")
        agent_id = call.data.get("agent_id")
        identifier = call.data.get("identifier")
        model = call.data.get("model")
        timeout_in_seconds = call.data.get("timeout_in_seconds")

        await send_prompt_command(
            hass, api_key, prompt, agent_id, identifier, model, timeout_in_seconds
        )

    hass.services.async_register(DOMAIN, "send_prompt", send_prompt)
    return True


async def async_unload_entry(hass, entry):
    hass.services.async_remove(DOMAIN, "send_prompt")
    return True

