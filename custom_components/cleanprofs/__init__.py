from __future__ import annotations

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.event import async_track_time_change

from .const import DOMAIN, CONF_ZIPCODE, CONF_HOUSE_NUMBER
from .coordinator import CleanProfsCoordinator

PLATFORMS = ["sensor", "binary_sensor", "calendar"]

# Set up the integration from a config entry (runs once when the integration is added/Loaded)
async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    hass.data.setdefault(DOMAIN, {})

    coordinator = CleanProfsCoordinator(
        hass,
        zipCode=entry.data[CONF_ZIPCODE],
        houseNumber=str(entry.data[CONF_HOUSE_NUMBER])
    )

    # First refresh so entities have data immediately after installation/restart
    result = coordinator.async_config_entry_first_refresh()
    print("DEBUG type first_refresh:", type(result), result)
    await result

    # Schedule an exact daily refresh at 00:05 local HA time
    async def dailyRefresh(now):
        await coordinator.async_request_refresh()
    
    removeListener = async_track_time_change(
        hass,
        dailyRefresh,
        hour=0,
        minute=5,
        second=0
    )

    hass.data[DOMAIN]["coordinator"] = coordinator
    hass.data[DOMAIN]["removeListener"] = removeListener

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

# Unload the integration and clean up scheduled listeners/entities
async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    data = hass.data.get(DOMAIN, {})
    if data.get("removeListener"):
        data["removeListener"]()
    
    unloaded = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unloaded and DOMAIN in hass.data:
        hass.data.pop(DOMAIN, None)
    
    return unloaded
