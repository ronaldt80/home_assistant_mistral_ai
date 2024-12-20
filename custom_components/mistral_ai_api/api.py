import logging
import requests
from datetime import datetime
from homeassistant.core import HomeAssistant
import asyncio
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def send_prompt_command(hass: HomeAssistant, api_key: str, prompt: str, agent_id: str, identifier: str, model: str, timeout_in_seconds: int):

    sensor = hass.data[DOMAIN].get("sensor")
    if sensor:
        sensor.set_state("processing")
        sensor.set_attribute("last_prompt", prompt)
        sensor.set_attribute("identifier", identifier)
        sensor.refresh_timestamp()
        sensor.async_write_ha_state()
    else:
        _LOGGER.error("Sensor instance not found in hass.data")

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

    timeout_to_use = timeout_in_seconds if timeout_in_seconds else 60

    try:
        response = await asyncio.wait_for(hass.async_add_executor_job(make_request), timeout=timeout_to_use)
        response.raise_for_status()
        response_data = response.json()
        if 'choices' in response_data and 'message' in response_data['choices'][0]:
            message_content = response_data['choices'][0]['message']['content']            

            if sensor:
                sensor.set_state("idle")
                sensor.set_attribute("last_response", message_content)                
                sensor.refresh_timestamp()
                sensor.async_write_ha_state()
            
            event_data = {"response": message_content, "identifier": identifier, "agent_id": agent_id if agent_id else ''}
            hass.bus.async_fire("mistral_ai_response", event_data)

            _LOGGER.error(f"Unexpected response structure: {response_data}")
    except asyncio.TimeoutError:
        _LOGGER.error("REST command timed out")
    except requests.exceptions.RequestException as e:
        _LOGGER.error(f"REST command error: {e}")
    except KeyError as e:
        _LOGGER.error(f"KeyError: {e}")