from __future__ import annotations

from homeassistant.components.binary_sensor import BinarySensorEntity, BinarySensorEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.device_registry import DeviceInfo

from .const import DOMAIN, FIXED_PRODUCTS
from .entity import CleanProfsBaseEntity
from .util import isoToday, nextDate

# Create binary sensor entities for the config entry.
async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry,async_add_entities: AddEntitiesCallback):
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]

    desc = BinarySensorEntityDescription(
        key="cleaning",
        translation_key= "cleaning",
        icon="mdi:trash-can"
    )

    async_add_entities([CleanProfsCleaningBinarySensor(coordinator, entry, desc)])
                       
class CleanProfsCleaningBinarySensor(CleanProfsBaseEntity, BinarySensorEntity):
    # Binary sensor that turns on when *any* product has to be cleaned
    _attr_has_entity_name = True
    
    def __init__(self, coordinator, entry: ConfigEntry, description: BinarySensorEntityDescription) -> None:
        super().__init__(coordinator, entry)
        self.entity_description = description
        self._attr_unique_id = f"{entry.entry_id}_cleaning"


    @property
    def is_on(self) -> bool:
        items = self.coordinator.data or []
        today = isoToday()

        for productName in FIXED_PRODUCTS:
            if nextDate(items, productName) == today:
                return True
        
        return False

    @property
    def extra_state_attributes(self):
        items = self.coordinator.data or []
        today = isoToday()

        cleaningProducts: list[str] = []
        nextDates: dict[str, str | None] = {}

        for productName in FIXED_PRODUCTS:
            nd = nextDate(items, productName)
            nextDates[productName] = nd
            if nd == today:
                cleaningProducts.append(productName)
        
        return {
            "cleaningProductToday": cleaningProducts,
            "nextdates": nextDates
        }
    