# sensor.py
from __future__ import annotations

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, FIXED_PRODUCTS
from .entity import CleanProfsBaseEntity
from .util import nextDate


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    coordinator = hass.data[DOMAIN]["coordinator"]

    entities = []
    for productName in FIXED_PRODUCTS:
        desc = SensorEntityDescription(
            key=f"cleaning_date_{productName}".lower(),
            name=f"{productName} cleaning date",
            icon="mdi:calendar-arrow-right",
        )
        entities.append(CleanProfsNextDateSensor(coordinator, entry, desc, productName))

    async_add_entities(entities)


class CleanProfsNextDateSensor(CleanProfsBaseEntity, SensorEntity):
    def __init__(
        self,
        coordinator,
        entry: ConfigEntry,
        description: SensorEntityDescription,
        productName: str,
    ) -> None:
        super().__init__(coordinator, entry)
        self.entity_description = description
        self.productName = productName
        self._attr_unique_id = f"{entry.entry_id}_cleaning_date_{productName}".lower()

    @property
    def native_value(self):
        return nextDate(self.coordinator.data or [], self.productName)