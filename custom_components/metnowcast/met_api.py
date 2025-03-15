""" Met.no API."""
from __future__ import annotations
import logging
from .const import NotFound, VERSION
import aiohttp


_LOGGER = logging.getLogger(__name__)

BASE_URL = "https://aa015h6buqvih86i1.api.met.no/weatherapi/nowcast/2.0"
REQUEST_HEADER = {
    "User-Agent": f"home-assistant-metnowcast/{VERSION} https://github.com/toringer/home-assistant-metnowcast"
}


class MetApi:
    """Met.no API"""

    def __init__(self) -> None:
        """Init"""

    async def get_now_cast(self, lat: float, lon: float):
        """Get Nowcast from met.no using aiohttp """
        url = f"{BASE_URL}/complete"
        param = {"lat": lat, "lon": lon}
        async with aiohttp.ClientSession() as session:
            async with session.get(url=url, params=param, headers=REQUEST_HEADER) as response:
                if response.status != 200:
                    raise NotFound
                data = await response.json()
                return data
