from __future__ import annotations

import aiohttp
import asyncio
from datetime import datetime

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import CleanProfsApi
from .const import DOMAIN

class CleanProfsCoordinator(DataUpdateCoordinator[list[dict]]):
    # Create the calendar entity from the config entry
    def __init__(self, hass: HomeAssistant, zipCode: str, houseNumber: str) -> None:
        self.zipCode = zipCode
        self.houseNumber = houseNumber
        self.api = CleanProfsApi(async_get_clientsession(hass))

        super().__init__(
            hass=hass,
            logger=__import__("logging").getLogger(__name__),
            name=f"{DOMAIN}",
            update_interval=None # refreshed via dialy trigger at 00:05
        )
    
    # Fetch fresh data from the API and return it; Home Assistant will store it in coordinator.data.
    async def _async_update_data(self) -> list[dict]:
        try:
            year = datetime.now().year
            startDate = f"{year}-01-01"
            endDate = f"{year+1}-01-01"

            items = await self.api.fetch_planning(self.zipCode, self.houseNumber, startDate, endDate)

            # Deduplicate results on (product_name, full_date).
            seen: set[tuple[str | None, str | None]] = set()
            out: list[dict] = []
            for item in items:
                key = (item.get("product_name"), item.get("full_date"))
                if key in seen:
                    continue
                seen.add(key)
                out.append(item)
            
            # Sort for stable ordering.
            out.sort(key=lambda r: ((r.get("product_name") or ""), (r.get("full_date") or "")))
            return out
        except (asyncio.TimeoutError, aiohttp.ClientError, aiohttp.ClientResponseError) as err:
            raise UpdateFailed(f"Connection error: {err}") from err
        except ValueError as err:
            raise UpdateFailed(f"Invalid  response: {err}") from err
        except Exception as err:
            raise UpdateFailed(f"Unexpected error: {err}")