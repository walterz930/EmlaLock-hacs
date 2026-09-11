from __future__ import annotations

from typing import Any
from urllib.parse import urlencode

from aiohttp import ClientResponseError
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import API_BASE


class EmlaLockApiError(Exception):
    """EmlaLock API error."""


class EmlaLockApi:
    def __init__(self, hass, user_id: str, api_key: str, holder_api_key: str | None = None):
        self.hass = hass
        self.user_id = user_id
        self.api_key = api_key
        self.holder_api_key = holder_api_key
        self.session = async_get_clientsession(hass)

    async def request(self, endpoint: str, **params: Any) -> dict[str, Any]:
        query = {"userid": self.user_id, "apikey": self.api_key, **params}
        if self.holder_api_key:
            query.setdefault("holderapikey", self.holder_api_key)
        url = f"{API_BASE}/{endpoint}?{urlencode(query)}"
        try:
            async with self.session.get(url, timeout=20) as response:
                data = await response.json(content_type=None)
                if response.status >= 400:
                    raise EmlaLockApiError(data.get("error", f"HTTP {response.status}"))
                if not isinstance(data, dict):
                    raise EmlaLockApiError("Invalid API response")
                return data
        except ClientResponseError as err:
            raise EmlaLockApiError(str(err)) from err

    async def info(self):
        return await self.request("info")

    async def action(self, endpoint: str, **params: Any):
        return await self.request(endpoint, **params)
