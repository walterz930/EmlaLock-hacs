from __future__ import annotations

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import CONF_HOLDER_API_KEY, DOMAIN
from .coordinator import EmlaLockCoordinator


class EmlaLockActionButton(CoordinatorEntity[EmlaLockCoordinator], ButtonEntity):
    _attr_has_entity_name = True

    def __init__(self, coordinator, entry_id, name, value, subtract=False):
        super().__init__(coordinator)
        self._value = value
        self._subtract = subtract
        self._attr_name = name
        self._attr_unique_id = f"{entry_id}_{name.lower().replace(' ', '_')}"

    async def async_press(self):
        endpoint = "sub" if self._subtract else "add"
        data = await self.coordinator.api.action(
            endpoint, value=self._value, text="Home Assistant"
        )
        self.coordinator.async_set_updated_data(data)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    coordinator: EmlaLockCoordinator = hass.data[DOMAIN]["entries"][entry.entry_id]["coordinator"]

    # Existing holder entries may have the holder role in their title even if
    # they were created before the holder API key field was added.
    is_holder = bool(entry.data.get(CONF_HOLDER_API_KEY)) or "(holder)" in entry.title.lower()
    if not is_holder:
        return

    entities = []
    for value, label in ((900, "15 minutes"), (3600, "1 hour"), (86400, "1 day")):
        entities.append(EmlaLockActionButton(coordinator, entry.entry_id, f"Add {label}", value))
        entities.append(EmlaLockActionButton(coordinator, entry.entry_id, f"Remove {label}", value, True))
    async_add_entities(entities)
