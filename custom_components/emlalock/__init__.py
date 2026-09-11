from __future__ import annotations

import voluptuous as vol
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import config_validation as cv

from .api import EmlaLockApi, EmlaLockApiError
from .const import CONF_API_KEY, CONF_HOLDER_API_KEY, CONF_USER_ID, DOMAIN
from .coordinator import EmlaLockCoordinator

PLATFORMS: list[Platform] = [Platform.SENSOR, Platform.BUTTON]

SERVICE_SCHEMA = vol.Schema({
    vol.Required("entry_id"): cv.string,
    vol.Required("value"): vol.Coerce(int),
    vol.Optional("text", default=""): cv.string,
})
RANDOM_SCHEMA = vol.Schema({
    vol.Required("entry_id"): cv.string,
    vol.Required("from_value"): vol.Coerce(int),
    vol.Required("to_value"): vol.Coerce(int),
})


async def async_setup(hass: HomeAssistant, config):
    hass.data.setdefault(DOMAIN, {"entries": {}, "services_registered": False})
    if not hass.data[DOMAIN]["services_registered"]:
        async def run_action(call: ServiceCall, endpoint: str, random: bool = False):
            entry = hass.data[DOMAIN]["entries"].get(call.data["entry_id"])
            if not entry:
                raise vol.Invalid("Unknown EmlaLock entry")
            api = entry["action_api"]
            try:
                if random:
                    result = await api.action(endpoint, **{"from": call.data["from_value"], "to": call.data["to_value"]})
                else:
                    params = {"value": call.data["value"]}
                    if call.data.get("text") and endpoint == "add":
                        params["text"] = call.data["text"][:49]
                    result = await api.action(endpoint, **params)
                entry["coordinator"].async_set_updated_data(result)
            except EmlaLockApiError as err:
                raise vol.Invalid(str(err)) from err

        for service_name, endpoint in {
            "add_time": "add", "subtract_time": "sub",
            "add_maximum": "addmaximum", "subtract_maximum": "submaximum",
            "add_minimum": "addminimum", "subtract_minimum": "subminimum",
            "add_requirements": "addrequirement", "subtract_requirements": "subrequirement",
        }.items():
            async def handler(call, ep=endpoint):
                await run_action(call, ep)
            hass.services.async_register(DOMAIN, service_name, handler, schema=SERVICE_SCHEMA)

        for service_name, endpoint in {
            "add_maximum_random": "addmaximumrandom", "subtract_maximum_random": "submaximumrandom",
            "add_minimum_random": "addminimumrandom", "subtract_minimum_random": "subminimumrandom",
            "add_requirements_random": "addrequirementrandom", "subtract_requirements_random": "subrequirementrandom",
        }.items():
            async def random_handler(call, ep=endpoint):
                await run_action(call, ep, True)
            hass.services.async_register(DOMAIN, service_name, random_handler, schema=RANDOM_SCHEMA)
        hass.data[DOMAIN]["services_registered"] = True
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    data = entry.data
    user_id = data[CONF_USER_ID]
    api_key = data[CONF_API_KEY]
    holder_api_key = data.get(CONF_HOLDER_API_KEY)

    if holder_api_key:
        action_api = EmlaLockApi(
            hass,
            user_id,
            api_key,
            holder_api_key=holder_api_key,
        )
    else:
        action_api = EmlaLockApi(hass, user_id, api_key)

    coordinator = EmlaLockCoordinator(hass, action_api)
    await coordinator.async_config_entry_first_refresh()
    hass.data[DOMAIN]["entries"][entry.entry_id] = {"coordinator": coordinator, "action_api": action_api}
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    hass.data[DOMAIN]["entries"].pop(entry.entry_id, None)
    return unload_ok
