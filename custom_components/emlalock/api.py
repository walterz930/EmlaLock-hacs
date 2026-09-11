from __future__ import annotations

from typing import Any
from urllib.parse import urlencode

from aiohttp import ClientError, ContentTypeError
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import API_BASE


class EmlaLockApiError(Exception):
    """EmlaLock API error."""


# EmlaLock only documents holderapikey for actions where a holder is
# authorized to perform the operation. Do not send it to every endpoint.
HOLDER_API_KEY_ENDPOINTS = frozenset(
    {
        "sub",
        "subrandom",
        "submaximum",
        "submaximumrandom",
        "subminimum",
        "subminimumrandom",
        "subrequirement",
        "subrequirementrandom",
    }
)


class EmlaLockApi:
    def __init__(self, hass, user_id: str, api_key: str, holder_api_key: str | None = None):
        self.hass = hass
        self.user_id = user_id
        self.api_key = api_key
        self.holder_api_key = holder_api_key.strip() if holder_api_key else None
        self.session = async_get_clientsession(hass)

    async def request(self, endpoint: str, **params: Any) -> dict[str, Any]:
        endpoint = endpoint.lstrip("/")
        query = {"userid": self.user_id, "apikey": self.api_key, **params}

        if self.holder_api_key and endpoint in HOLDER_API_KEY_ENDPOINTS:
            query["holderapikey"] = self.holder_api_key

        url = f"{API_BASE}/{endpoint}?{urlencode(query)}"
        try:
            async with self.session.get(url, timeout=20) as response:
                try:
                    data = await response.json(content_type=None)
                except (ContentTypeError, ValueError) as err:
                    raise EmlaLockApiError(
                        f"Invalid response from EmlaLock (HTTP {response.status})"
                    ) from err

                if not isinstance(data, dict):
                    raise EmlaLockApiError("Invalid API response")

                if response.status >= 400 or data.get("error"):
                    raise EmlaLockApiError(
                        data.get("error", f"HTTP {response.status}")
                    )
                return data
        except TimeoutError as err:
            raise EmlaLockApiError("EmlaLock API request timed out") from err
        except ClientError as err:
            raise EmlaLockApiError(f"EmlaLock API request failed: {err}") from err

    async def info(self):
        return await self.request("info")

    async def action(self, endpoint: str, **params: Any):
        return await self.request(endpoint, **params)
