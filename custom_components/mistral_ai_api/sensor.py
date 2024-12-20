from datetime import datetime
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity import generate_entity_id
from homeassistant.core import HomeAssistant
from .const import DOMAIN, VERSION

class MistralAiSensor(Entity):

    _attr_has_entity_name = True
    def __init__(self, hass: HomeAssistant, data):
        self.entity_id = generate_entity_id(entity_id_format="sensor.{}",name="mistral_ai_api",hass=hass)

        self.hass = hass
        self._state = data.get("state")
        self._attributes = {
            "last_response": data.get("response"),
            "last_prompt": data.get("prompt"),
            "timestamp": datetime.now().timestamp(),
            "identifier": data.get("identifier")
        }

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            name="MistralAiApi",
            sw_version=VERSION,
            identifiers={
                (
                    DOMAIN,
                    "mistral_ai",
                )
            },
        )

    def has_entity_name(self):
        return True

    @property
    def name(self):
        return self.device_info["name"]

    @property
    def state(self):
        return self._state

    @property
    def extra_state_attributes(self):
        return self._attributes

    def set_state(self, state: str):
        self._state = state
        
    def set_attribute(self, key: str, value: any):
        self._attributes[key] = value

    def refresh_timestamp(self):
        self.set_attribute("timestamp", datetime.now().timestamp())