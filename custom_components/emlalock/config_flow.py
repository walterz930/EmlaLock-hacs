from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_API_KEY

from .api import EmlaLockApi, EmlaLockApiError
from .const import (
    CONF_ROLE,
    CONF_USER_ID,
    CONF_WEARER_API_KEY,
    CONF_WEARER_USER_ID,
    DOMAIN,
    ROLE_HOLDER,
    ROLE_WEARER,
)


class EmlaLockConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            try:
                info = await EmlaLockApi(
                    self.hass,
                    user_input[CONF_USER_ID],
                    user_input[CONF_API_KEY],
                ).info()
            except EmlaLockApiError:
                errors["base"] = "invalid_auth"
            else:
                self._user_input = user_input
                if user_input[CONF_ROLE] == ROLE_HOLDER:
                    return await self.async_step_holder()

                return await self._create_entry(info)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_USER_ID): str,
                    vol.Required(CONF_API_KEY): str,
                    vol.Required(CONF_ROLE, default=ROLE_WEARER): vol.In(
                        [ROLE_WEARER, ROLE_HOLDER]
                    ),
                }
            ),
            errors=errors,
        )

    async def async_step_holder(self, user_input=None):
        errors = {}

        if user_input is not None:
            try:
                await EmlaLockApi(
                    self.hass,
                    user_input[CONF_WEARER_USER_ID],
                    user_input[CONF_WEARER_API_KEY],
                ).info()
            except EmlaLockApiError:
                errors["base"] = "invalid_wearer_auth"
            else:
                self._user_input.update(user_input)
                try:
                    info = await EmlaLockApi(
                        self.hass,
                        self._user_input[CONF_USER_ID],
                        self._user_input[CONF_API_KEY],
                    ).info()
                except EmlaLockApiError:
                    errors["base"] = "invalid_auth"
                else:
                    return await self._create_entry(info)

        return self.async_show_form(
            step_id="holder",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_WEARER_USER_ID): str,
                    vol.Required(CONF_WEARER_API_KEY): str,
                }
            ),
            errors=errors,
        )

    async def _create_entry(self, info):
        user = info.get("user", {})
        username = user.get("username", self._user_input[CONF_USER_ID])
        await self.async_set_unique_id(
            f"{user.get('userid', self._user_input[CONF_USER_ID])}-{self._user_input[CONF_ROLE]}"
        )
        self._abort_if_unique_id_configured()
        return self.async_create_entry(
            title=f"EmlaLock - {username} ({self._user_input[CONF_ROLE]})",
            data=self._user_input,
        )
