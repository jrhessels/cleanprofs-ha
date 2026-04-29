from __future__ import annotations
import aiohttp

# Import API url
from .const import API_URL

class CleanProfsApi:
    # Create a small API client using Home Assistant's aiohttp session.
    def __init__(self, session: aiohttp.ClientSession) -> None:
        self._session = session
    
    # Fetch planning data from the CleanProfs endpoint and return a list of dict items.
    async def fetch_planning(
            self,
            zipCode: str,
            houseNumber: str,
            startDate: str,
            endDate: str
    ) ->list[dict]:
        params = {
            "zipcode": zipCode,
            "house_number": houseNumber,
            "start_date": startDate,
            "end_date": endDate
        }
        async with self._session.get(
            API_URL,
            params=params,
            timeout=aiohttp.ClientTimeout(total=30)
        ) as resp:
            resp.raise_for_status()
            data = await resp.json()
        
        # Ensure we always return a predictable type (list[dict]).
        if not isinstance(data,list):
            return[]
        return[x for x in data if isinstance(x, dict)]