""" Met.no API."""
from __future__ import annotations
from datetime import datetime
import logging
import requests
from requests_oauthlib import OAuth2Session
from .const import NotFound

_LOGGER = logging.getLogger(__name__)

BASE_URL = "https://api.met.no/weatherapi/nowcast/2.0"
REQUEST_HEADER = {
    "User-Agent": "home-assistant-metnowcast https://github.com/toringer/home-assistant-metnowcast"
}


class MetApi:
    """Met.no API"""

    def __init__(self) -> None:
        """Init"""
        self._session: OAuth2Session = None
        self._session_expires_at: datetime = datetime.now()

    def get_complete(self, lat: float, lon: float):
        """Get complete forecast"""
        url = f"{BASE_URL}/complete"
        param = {"lat": lat, "lon": lon}
        response = requests.get(url=url, params=param, headers=REQUEST_HEADER)
        if response.status_code != 200:
            raise NotFound

        data = response.json()
        return data
