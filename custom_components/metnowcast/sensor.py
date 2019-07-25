"""Support for Yr.no weather service."""
import asyncio
import logging

from xml.parsers.expat import ExpatError

import aiohttp
import async_timeout
import voluptuous as vol
import datetime

import homeassistant.helpers.config_validation as cv
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import (
    CONF_LATITUDE, CONF_LONGITUDE, ATTR_ATTRIBUTION)
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.event import (async_track_utc_time_change,
                                         async_call_later)
from homeassistant.util import dt as dt_util

_LOGGER = logging.getLogger(__name__)


SCAN_INTERVAL = datetime.timedelta(minutes=7)

ATTRIBUTION = "Weather now cast from met.no, delivered by the Norwegian " \
              "Meteorological Institute."
# https://api.met.no/license_data.html




PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_LATITUDE): cv.latitude,
    vol.Optional(CONF_LONGITUDE): cv.longitude
})


async def async_setup_platform(hass, config, async_add_entities,
                               discovery_info=None):
    """Set up the Yr.no sensor."""
    latitude = config.get(CONF_LATITUDE, hass.config.latitude)
    longitude = config.get(CONF_LONGITUDE, hass.config.longitude)

    if None in (latitude, longitude):
        _LOGGER.error("Latitude or longitude not set in Home Assistant config")
        return False

    coordinates = {
        'lat': str(latitude),
        'lon': str(longitude)
    }

    met_api = MetData(hass, coordinates)
    sensor = YrSensor(met_api)
    await sensor.async_update()
    async_add_entities([sensor])


class YrSensor(Entity):
    """Representation of an Yr.no sensor."""

    def __init__(self, met_api):
        """Initialize the sensor."""
        self._met_api = met_api
        self._state = 0
        self._unit_of_measurement = '???'
        self._forecast = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return 'met.no now cast'

    @property
    def state(self):
        """Return the state of the device."""
        return self._state

    @property
    def should_poll(self):
        """No polling needed."""
        return True

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        return {
            ATTR_ATTRIBUTION: ATTRIBUTION,
            'forecast': self._forecast
        }

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return "mdi:package"

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement of this entity, if any."""
        return self._unit_of_measurement

    async def async_update(self):
        """Retrieve latest state."""
        data = await self._met_api.fetching_data()
        forecast = []
        for time_entry in data['product']['time']:
            valid_from = dt_util.parse_datetime(time_entry['@from'])
            valid_to = dt_util.parse_datetime(time_entry['@to'])
            unit = time_entry['location']['precipitation']['@unit']
            value = time_entry['location']['precipitation']['@value']
            forecast.append({'unit': unit,'value': value, 'from': valid_from, 'to': valid_to})

        _LOGGER.info("met now cast data updated")
        self._forecast = forecast
        self._state = max(self._forecast, key=lambda ev: ev['value'])['value']
        self._unit_of_measurement = self._forecast[0]['unit']


class MetData:
    """Get the latest data and updates the states."""

    def __init__(self, hass, coordinates):
        """Initialize the data object."""
        self._url = 'https://api.met.no/weatherapi/nowcast/0.9/'
        self._urlparams = coordinates
        self.data = {}
        self.hass = hass

    async def fetching_data(self, *_):
        """Get the latest data from yr.no."""
        import xmltodict

        def try_again(err: str):
            """Retry in 15 to 20 minutes."""
            minutes = 15 + randrange(6)
            _LOGGER.error("Retrying in %i minutes: %s", minutes, err)
        try:
            websession = async_get_clientsession(self.hass)
            with async_timeout.timeout(10):
                resp = await websession.get(
                    self._url, params=self._urlparams)
            if resp.status != 200:
                try_again('{} returned {}'.format(resp.url, resp.status))
                return
            text = await resp.text()

        except (asyncio.TimeoutError, aiohttp.ClientError) as err:
            try_again(err)
            return

        try:
            self.data = xmltodict.parse(text)['weatherdata']
            return self.data
        except (ExpatError, IndexError) as err:
            try_again(err)
            return

