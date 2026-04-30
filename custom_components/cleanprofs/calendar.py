from __future__ import annotations

from datetime import datetime, timedelta

from homeassistant.components.calendar import CalendarEntity, CalendarEvent
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.util import dt as dt_util

from .const import DOMAIN, FIXED_PRODUCTS
from .util import _norm, parseIsoDate

# Create the calendar entity for the config entry.
async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback):
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    async_add_entities([CleanProfsCalendar(coordinator, entry)])

class CleanProfsCalendar(CoordinatorEntity, CalendarEntity):
    # Calendat entity that exposes pickup dates as all-day events,
    _attr_has_entity_name = True
    _attr_translation_key = "schedule"
    _attr_icon = "mdi:calendar-trash"
    _attr_unique_id = "cleanprofs_calendar"

    # Initialize the calendar with a coordinator and the fixed product set.
    def __init__(self, coordinator) -> None:
        super().__init__(coordinator)
        self.products = set(FIXED_PRODUCTS)
        self._attr_unique_id = "cleanprofs_calendar"
        self._event: CalendarEvent | None = None
    
    # Return the next upcoming event; HA calls this to determine the calendar entity state.
    @property
    def event(self) -> CalendarEvent | None:
        return self._event

    # Recompute the next upcoming event and store it in self._event.
    async def async_update(self) -> None:
        now = dt_util.now()
        events = await self.async_get_events(
            self.hass,
            start_date=now - timedelta(days=1),
            end_date=now + timedelta(days=365),
        )
        self._event = events[0] if events else None  

    # Return calendar events within the requested datetime range.
    async def async_get_events(
        self,
        hass: HomeAssistant,
        start_date: datetime,
        end_date: datetime,
    ):
        items = self.coordinator.data or []
        tz = dt_util.DEFAULT_TIME_ZONE  # use HA's configured timezone

        events: list[CalendarEvent] = []
        for item in items:
            productNameApi = item.get("product_name")
            if _norm(productNameApi) not in self.products:
                continue

            fullDate = item.get("full_date")
            if not isinstance(fullDate, str):
                continue

            d = parseIsoDate(fullDate)
            if d is None:
                continue

            # Create an all-day event (00:00 -> next day 00:00) in local HA timezone.
            start = datetime(d.year, d.month, d.day, 7, 0, 0, tzinfo=tz)
            end = datetime(d.year, d.month, d.day, 19, 0, 0, tzinfo=tz)

            # Only include events that overlap the requested range.
            if end <= start_date or start >= end_date:
                continue

            p = _norm(productNameApi)
            events.append(
                CalendarEvent(
                    summary=f"Cleaning: {p}",
                    start=start,
                    end=end,
                    description=f"Put {p} bin at the curb (07:00-19:00)",
                    location="Aan de straat",
                )
            )

        events.sort(key=lambda e: e.start)
        return events
