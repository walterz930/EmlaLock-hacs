from __future__ import annotations

from datetime import datetime, timedelta, timezone

from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.event import async_track_time_interval
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import CONF_USER_ID, DOMAIN
from .coordinator import EmlaLockCoordinator


def _session(coordinator):
    return (coordinator.data or {}).get("chastitysession") or {}


def _timestamp(value):
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        pass
    text = str(value).strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.timestamp()


def _format_duration(value):
    if value is None or value == "":
        return None
    try:
        total = max(0, int(float(value)))
    except (TypeError, ValueError):
        return str(value)
    days, remainder = divmod(total, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{days:02d} {hours:02d} {minutes:02d} {seconds:02d}"


class EmlaLockBase(CoordinatorEntity[EmlaLockCoordinator]):
    _attr_has_entity_name = True

    def __init__(self, coordinator, user_id, unique_suffix):
        super().__init__(coordinator)
        self._attr_unique_id = f"{user_id}_{unique_suffix}"

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self.coordinator.api.user_id)},
            "name": "EmlaLock",
            "manufacturer": "EmlaLock",
        }


class EmlaLockTimeRemaining(EmlaLockBase, SensorEntity):
    _attr_name = "Time remaining"

    @property
    def native_value(self):
        end = _timestamp(_session(self.coordinator).get("enddate"))
        if end is None:
            return None
        remaining = max(0, int(end - datetime.now(timezone.utc).timestamp()))
        return _format_duration(remaining)

    async def async_added_to_hass(self) -> None:
        await super().async_added_to_hass()
        self._unsub_timer = async_track_time_interval(
            self.hass, self._async_update_time, timedelta(seconds=1)
        )

    async def async_will_remove_from_hass(self) -> None:
        if hasattr(self, "_unsub_timer"):
            self._unsub_timer()
        await super().async_will_remove_from_hass()

    async def _async_update_time(self, _now) -> None:
        self.async_write_ha_state()

    @property
    def extra_state_attributes(self):
        s = _session(self.coordinator)
        return {k: s.get(k) for k in (
            "chastitysessionid", "wearerid", "holderid", "status", "duration",
            "minduration", "maxduration", "requirements", "startdate", "enddate",
            "timeinlock", "lastverification", "incleaning",
        )}


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

    @property
    def native_value(self):
        return _format_duration(_session(self.coordinator).get("maxduration"))


class EmlaLockMinimum(EmlaLockBase, SensorEntity):
    _attr_name = "Minimum duration"

    @property
    def native_value(self):
        return _format_duration(_session(self.coordinator).get("minduration"))


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
):
    coordinator: EmlaLockCoordinator = hass.data[DOMAIN]["entries"][entry.entry_id]["coordinator"]
    user_id = entry.data[CONF_USER_ID]
    async_add_entities([
        EmlaLockTimeRemaining(coordinator, user_id, "remaining"),
        EmlaLockSession(coordinator, user_id, "session"),
        EmlaLockRequirementLinks(coordinator, user_id, "requirements"),
        EmlaLockMaximum(coordinator, user_id, "maximum"),
        EmlaLockMinimum(coordinator, user_id, "minimum"),
    ])
