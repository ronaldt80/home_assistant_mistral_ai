import logging
import requests
from datetime import datetime
import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from homeassistant.const import CONF_NAME, CONF_API_KEY
from homeassistant.core import HomeAssistant
import asyncio
from homeassistant.config_entries import ConfigEntry

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

    async def send_prompt_command(call):
        prompt = call.data.get("prompt")
        agent_id = call.data.get("agent_id")
        identifier = call.data.get("identifier")
        model = call.data.get("model")

        current_state = hass.states.get("sensor.mistral_ai")
        current_attributes = current_state.attributes if current_state else {}
        new_attributes = {**current_attributes, "timestamp": datetime.now().timestamp(), "identifier": identifier}
        hass.states.async_set("sensor.mistral_ai", "processing", new_attributes)        

        headers = {
            "content-type": "application/json",
            "accept": "application/json",
            "authorization": f"Bearer {api_key}",
        }

        url = "https://api.mistral.ai/v1/agents/completions" if agent_id else "https://api.mistral.ai/v1/chat/completions"

        if agent_id:
            payload = {
                "agent_id": agent_id,
                "messages": [{"role": "user", "content": prompt}],
            }
        else:
            payload = {
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
            }

        def make_request():
            response = requests.post(url, headers=headers, json=payload, timeout=60)
            return response

        message_content = ''

        try:
            response = await asyncio.wait_for(hass.async_add_executor_job(make_request), timeout=60)
            response.raise_for_status()
            response_data = response.json()
            if 'choices' in response_data and 'message' in response_data['choices'][0]:
                message_content = response_data['choices'][0]['message']['content']
                current_state = hass.states.get("sensor.mistral_ai")
                current_attributes = current_state.attributes if current_state else {}
                new_attributes = {**current_attributes, "timestamp": datetime.now().timestamp()}
                hass.states.async_set("sensor.mistral_ai", "done", new_attributes)
                
                event_data = {"response": message_content, "identifier": identifier, "agent_id": agent_id if agent_id else ''}
                hass.bus.async_fire("mistral_ai_response", event_data)
            else:
                _LOGGER.error(f"Unexpected response structure: {response_data}")
        except asyncio.TimeoutError:
            _LOGGER.error("REST command timed out")
        except requests.exceptions.RequestException as e:
            _LOGGER.error(f"REST command error: {e}")
        except KeyError as e:
            _LOGGER.error(f"KeyError: {e}")

    hass.services.async_register(DOMAIN, "send_prompt", send_prompt_command)
    return True

async def async_unload_entry(hass, entry):
    hass.services.async_remove(DOMAIN, "send_prompt")
    return True