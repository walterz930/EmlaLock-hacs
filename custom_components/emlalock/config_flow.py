from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_API_KEY

from .api import EmlaLockApi, EmlaLockApiError
from .const import CONF_HOLDER_API_KEY, CONF_USER_ID, DOMAIN


class EmlaLockConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            try:
                await EmlaLockApi(
                    self.hass,
                    user_input[CONF_USER_ID],
                    user_input[CONF_API_KEY],
                ).info()
                if user_input.get(CONF_HOLDER_API_KEY):
                    await EmlaLockApi(
                        self.hass,
                        user_input[CONF_USER_ID],
                        user_input[CONF_API_KEY],
                        holder_api_key=user_input[CONF_HOLDER_API_KEY],
                    ).info()
            except EmlaLockApiError:
                errors["base"] = "invalid_auth"
            else:
                user = user_input[CONF_USER_ID]
                role = "holder" if user_input.get(CONF_HOLDER_API_KEY) else "wearer"
                await self.async_set_unique_id(f"{user}-{role}")
                self._abort_if_unique_id_configured()
                return self.async_create_entry(
                    title=f"EmlaLock - {user} ({role})",
                    data=user_input,
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_USER_ID): str,
                    vol.Required(CONF_API_KEY): str,
                    vol.Optional(CONF_HOLDER_API_KEY): str,
                }
            ),
            errors=errors,
        )
