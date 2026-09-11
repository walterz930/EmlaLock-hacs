from __future__ import annotations

from datetime import datetime, timezone

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTime
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import EmlaLockCoordinator


def _session(coordinator):
    return (coordinator.data or {}).get("chastitysession") or {}


class EmlaLockBase(CoordinatorEntity[EmlaLockCoordinator]):
    _attr_has_entity_name = True

    def __init__(self, coordinator, entry_id, unique_suffix):
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry_id}_{unique_suffix}"
        self._entry_id = entry_id

    @property
    def device_info(self):
        return {"identifiers": {(DOMAIN, self._entry_id)}, "name": "EmlaLock"}


class EmlaLockTimeRemaining(EmlaLockBase, SensorEntity):
    _attr_name = "Time remaining"
    _attr_native_unit_of_measurement = UnitOfTime.SECONDS
    _attr_device_class = SensorDeviceClass.DURATION
    _attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def native_value(self):
        end = _session(self.coordinator).get("enddate")
        if not end:
            return None
        return max(0, int(end - datetime.now(timezone.utc).timestamp()))

    @property
    def extra_state_attributes(self):
        s = _session(self.coordinator)
        return {k: s.get(k) for k in ("chastitysessionid", "wearerid", "holderid", "status", "duration", "minduration", "maxduration", "requirements", "startdate", "enddate", "timeinlock", "lastverification", "incleaning")}


class EmlaLockSession(EmlaLockBase, SensorEntity):
    _attr_name = "Session"

    @property
    def native_value(self):
        return "active" if _session(self.coordinator).get("status") else "inactive"


class EmlaLockRequirementLinks(EmlaLockBase, SensorEntity):
    _attr_name = "Requirement links"
    _attr_native_unit_of_measurement = "links"
    _attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def native_value(self):
        return _session(self.coordinator).get("requirements")


class EmlaLockMaximum(EmlaLockBase, SensorEntity):
    _attr_name = "Maximum duration"
    _attr_native_unit_of_measurement = UnitOfTime.SECONDS
    _attr_device_class = SensorDeviceClass.DURATION

    @property
    def native_value(self):
        return _session(self.coordinator).get("maxduration")


class EmlaLockMinimum(EmlaLockBase, SensorEntity):
    _attr_name = "Minimum duration"
    _attr_native_unit_of_measurement = UnitOfTime.SECONDS
    _attr_device_class = SensorDeviceClass.DURATION

    @property
    def native_value(self):
        return _session(self.coordinator).get("minduration")


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback):
    coordinator: EmlaLockCoordinator = hass.data[DOMAIN]["entries"][entry.entry_id]["coordinator"]
    async_add_entities([
        EmlaLockTimeRemaining(coordinator, entry.entry_id, "remaining"),
        EmlaLockSession(coordinator, entry.entry_id, "session"),
        EmlaLockRequirementLinks(coordinator, entry.entry_id, "requirements"),
        EmlaLockMaximum(coordinator, entry.entry_id, "maximum"),
        EmlaLockMinimum(coordinator, entry.entry_id, "minimum"),
    ])
