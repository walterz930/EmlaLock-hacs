from __future__ import annotations

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .api import EmlaLockApiError
from .const import DOMAIN
from .coordinator import EmlaLockCoordinator


class EmlaLockActionButton(CoordinatorEntity[EmlaLockCoordinator], ButtonEntity):
    _attr_has_entity_name = True

    def __init__(self, coordinator, user_id, name, value, subtract=False):
        super().__init__(coordinator)
        self._value = value
        self._subtract = subtract
        self._attr_name = name
        self._attr_unique_id = f"{user_id}_{name.lower().replace(' ', '_')}"
        self._attr_entity_registry_enabled_default = True

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self.coordinator.api.user_id)},
            "name": "EmlaLock",
            "manufacturer": "EmlaLock",
        }

    @property
    def available(self) -> bool:
        if not super().available:
            return False
        if self._subtract and not self.coordinator.api.holder_api_key:
            return False
        return True

    async def async_press(self) -> None:
        endpoint = "sub" if self._subtract else "add"
        session = (self.coordinator.data or {}).get("chastitysession") or {}
        params = {
            "value": self._value,
            "text": "Home Assistant",
        }

        # Pass the current session dates to the EmlaLock action API when they
        # are available. This lets the API keep the action tied to the session
        # start/end dates instead of only receiving the duration value.
        if session.get("startdate") is not None:
            params["startdate"] = session["startdate"]
        if session.get("enddate") is not None:
            params["enddate"] = session["enddate"]

        try:
            await self.coordinator.api.action(endpoint, **params)
        except EmlaLockApiError:
            return

        await self.coordinator.async_request_refresh()


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    coordinator: EmlaLockCoordinator = hass.data[DOMAIN]["entries"][entry.entry_id]["coordinator"]
    user_id = entry.data["user_id"]

    entities = []
    for value, label in (
        (3600, "1 hour"),
        (86400, "1 day"),
    ):
        entities.append(
            EmlaLockActionButton(coordinator, user_id, f"Add {label}", value)
        )
        entities.append(
            EmlaLockActionButton(
                coordinator,
                user_id,
                f"Remove {label}",
                value,
                subtract=True,
            )
        )

    async_add_entities(entities)
