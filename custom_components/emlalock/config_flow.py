from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_API_KEY

from .api import EmlaLockApi, EmlaLockApiError
from .const import CONF_ROLE, CONF_USER_ID, CONF_WEARER_API_KEY, CONF_WEARER_USER_ID, DOMAIN, ROLE_HOLDER, ROLE_WEARER


class EmlaLockConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input:
            try:
                data = await EmlaLockApi(self.hass, user_input[CONF_USER_ID], user_input[CONF_API_KEY]).info()
                if user_input[CONF_ROLE] == ROLE_HOLDER:
                    if not user_input.get(CONF_WEARER_USER_ID) or not user_input.get(CONF_WEARER_API_KEY):
                        errors["base"] = "wearer_credentials_required"
                    else:
                        await EmlaLockApi(self.hass, user_input[CONF_WEARER_USER_ID], user_input[CONF_WEARER_API_KEY]).info()
                if errors:
                    raise EmlaLockApiError(errors["base"])
            except EmlaLockApiError as err:
                errors.setdefault("base", "wearer_credentials_required" if str(err) == "wearer_credentials_required" else "invalid_auth")
            else:
                user = data.get("user", {})
                username = user.get("username", user_input[CONF_USER_ID])
                await self.async_set_unique_id(f"{user.get('userid', user_input[CONF_USER_ID])}-{user_input[CONF_ROLE]}")
                self._abort_if_unique_id_configured()
                return self.async_create_entry(title=f"EmlaLock - {username} ({user_input[CONF_ROLE]})", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_USER_ID): str,
                vol.Required(CONF_API_KEY): str,
                vol.Required(CONF_ROLE, default=ROLE_WEARER): vol.In([ROLE_WEARER, ROLE_HOLDER]),
                vol.Optional(CONF_WEARER_USER_ID): str,
                vol.Optional(CONF_WEARER_API_KEY): str,
            }),
            errors=errors,
        )
