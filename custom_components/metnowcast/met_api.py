""" Met.no API."""
from __future__ import annotations
import logging
from .const import NotFound, VERSION
from homeassistant.helpers.aiohttp_client import async_get_clientsession


_LOGGER = logging.getLogger(__name__)

BASE_URL = "https://aa015h6buqvih86i1.api.met.no/weatherapi/nowcast/2.0"
REQUEST_HEADER = {
    "User-Agent": f"home-assistant-metnowcast/{VERSION} https://github.com/toringer/home-assistant-metnowcast"
}


class MetApi:
    """Met.no API"""

    def __init__(self, hass) -> None:
        """Init with Home Assistant instance."""
        self.hass = hass

    async def get_now_cast(self, lat: float, lon: float):
        """Get Nowcast from met.no using Home Assistant's shared aiohttp session."""
        url = f"{BASE_URL}/complete"
        param = {"lat": lat, "lon": lon}
        session = async_get_clientsession(self.hass)
        async with session.get(url=url, params=param, headers=REQUEST_HEADER) as response:
            if response.status != 200:
                raise NotFound
            data = await response.json()
            return data
