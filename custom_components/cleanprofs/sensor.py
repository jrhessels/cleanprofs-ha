from __future__ import annotations

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.device_registry import DeviceInfo

from .const import DOMAIN, FIXED_PRODUCTS
from .util import nextDate

# Create sensor entities from the config entry
async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback):
    coordinator = hass.data[DOMAIN]["coordinator"]

    entities = []
    for productName in FIXED_PRODUCTS:
        desc = SensorEntityDescription(
            key=f"cleanprofs_{productName}",
            name=f"Cleanprofs {productName}",
            icon="mdi:calendar-arrow-right"
        )
        entities.append(CleanProfsNextDateSensor(coordinator, desc, productName))
    async_add_entities(entities)

class CleanProfsNextDateSensor(CoordinatorEntity, SensorEntity):
    # Sensor that exposes the next pickup date (YYYY-MM-DD) for a single product
    _attr_has_entity_name = True

    # Initialize the sensor with a coordinator and fixed product name.
    def __init__(self, coordinator, description: SensorEntityDescription, productName: str) -> None:
        super().__init__(coordinator)
        self.entity_description = description
        self.productName = productName
        self._attr_unique_id = f"cleanprofs_{productName}".lower()
    
    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            identifiers={(DOMAIN, "cleanprofs_device")},
            name="CleanProfs",
            manufacturer="CleanProfs",
            model="Planning API",
        )

    # Return the sensor value (next pickup date or None/unknown)
    @property
    def native_value(self):
        return nextDate(self.coordinator.data or [], self.productName)
