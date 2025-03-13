""" Met.no API."""
from __future__ import annotations
from datetime import datetime
import logging
import requests
from .const import NotFound, VERSION

_LOGGER = logging.getLogger(__name__)

BASE_URL = "https://aa015h6buqvih86i1.api.met.no/weatherapi/nowcast/2.0"
REQUEST_HEADER = {
    "User-Agent": f"home-assistant-metnowcast/{VERSION} https://github.com/toringer/home-assistant-metnowcast"
}


class MetApi:
    """Met.no API"""

    def __init__(self) -> None:
        """Init"""

    def get_complete(self, lat: float, lon: float):
        """Get complete forecast"""
        url = f"{BASE_URL}/complete"
        param = {"lat": lat, "lon": lon}
        response = requests.get(url=url, params=param, headers=REQUEST_HEADER)
        _LOGGER.debug(f"REQUEST_HEADER: {REQUEST_HEADER}")
        if response.status_code != 200:
            raise NotFound

        data = response.json()
        return data
