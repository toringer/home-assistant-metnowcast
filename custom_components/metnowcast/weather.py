"""Support for met.no nowcast weather service."""

import logging
import datetime
import random

from homeassistant.const import (
    CONF_LATITUDE,
    CONF_LONGITUDE,
    CONF_NAME,
    TEMP_CELSIUS,
    SPEED_METERS_PER_SECOND,
    LENGTH_MILLIMETERS
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.device_registry import DeviceEntryType
from homeassistant.util import dt as dt_util
from homeassistant.components.weather import (
    Forecast,
    WeatherEntity,
)
from .met_api import MetApi
from .const import (
    ATTRIBUTION,
    DOMAIN,
    NAME,
    CONDITIONS_MAP,
    ATTR_RADAR_COVERAGE,
    ATTR_HAS_PRECIPITATION
)

_LOGGER = logging.getLogger(__name__)
SCAN_INTERVAL = datetime.timedelta(minutes=7)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Setup weather platform."""
    api: MetApi = hass.data[DOMAIN]["api"]
    lat = entry.data[CONF_LATITUDE]
    lon = entry.data[CONF_LONGITUDE]
    name = entry.data[CONF_NAME]
    sensors = [NowcastWeather(hass, api, name, lat, lon)]
    async_add_entities(sensors, True)


def format_condition(condition: str) -> str:
    """Return condition from dict CONDITIONS_MAP."""
    for key, value in CONDITIONS_MAP.items():
        if condition in value:
            return key
    return condition


class NowcastWeather(WeatherEntity):
    """Representation of a Nowcast sensor."""

    _attr_native_temperature_unit = TEMP_CELSIUS
    _attr_native_wind_speed_unit = SPEED_METERS_PER_SECOND
    _attr_native_precipitation_unit= LENGTH_MILLIMETERS

    def __init__(
        self,
        hass: HomeAssistant,
        met_api: MetApi,
        location_name: str,
        lat: float,
        lon: float,
    ):
        """Initialize the sensor."""
        self._hass = hass
        self._met_api = met_api
        self.location_name = location_name
        self.lat = lat
        self.lon = lon
        self._raw_data = None
        self._forecast: list[Forecast] = None
        self._first_timeserie = None
        self._radar_coverage = ""
        self._has_precipitation = False


    @property
    def force_update(self) -> str:
        """Force update."""
        return True

    @property
    def unique_id(self) -> str:
        """Return unique ID."""
        return f"nowcast-{self.location_name}"

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return f"{NAME}: {self.location_name}"

    @property
    def condition(self) -> str:
        """Return the current condition."""
        condition = self._first_timeserie["data"]["next_1_hours"]["summary"][
            "symbol_code"
        ]
        return format_condition(condition)

    @property
    def native_temperature(self) -> float:
        """Return the temperature."""
        return self._first_timeserie["data"]["instant"]["details"]["air_temperature"]

    @property
    def native_pressure(self) -> float:
        """Return the pressure."""
        return None

    @property
    def humidity(self) -> float:
        """Return the humidity."""
        return self._first_timeserie["data"]["instant"]["details"]["relative_humidity"]

    @property
    def native_wind_speed(self) -> float:
        """Return the wind speed."""
        return self._first_timeserie["data"]["instant"]["details"]["wind_speed"]

    @property
    def wind_bearing(self) -> float:
        """Return the wind direction."""
        return self._first_timeserie["data"]["instant"]["details"][
            "wind_from_direction"
        ]

    @property
    def attribution(self) -> str:
        """Return the attribution."""
        return ATTRIBUTION

    @property
    def forecast(self) -> list[Forecast]:
        """Return the forecast array."""
        return self._forecast

    @property
    def device_info(self):
        """Return the device_info of the device."""
        device_info = DeviceInfo(
            identifiers={(DOMAIN, self.location_name)},
            entry_type=DeviceEntryType.SERVICE,
            name=f"{NAME}: {self.location_name}",
            manufacturer="Met.no",
            model="Nowcast",
            configuration_url="https://www.met.no/en",
        )
        return device_info

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return {
            ATTR_RADAR_COVERAGE: self._radar_coverage,
            ATTR_HAS_PRECIPITATION: self._has_precipitation
        }

    async def async_update(self):
        """Retrieve latest state."""
        self._raw_data = await self._hass.async_add_executor_job(
            self._met_api.get_complete, self.lat, self.lon
        )
        self._radar_coverage = self._raw_data["properties"]["meta"]["radar_coverage"]
        timeseries = self._raw_data["properties"]["timeseries"]
        self._forecast = []
        self._has_precipitation = False

        for timeserie in timeseries:
            details = timeserie["data"]["instant"]["details"]

            temp = None
            if "air_temperature" in details:
                temp = details["air_temperature"]

            precipitation_rate = None
            if "precipitation_rate" in details:
                precipitation_rate = details["precipitation_rate"]
            if self.location_name == "debug":
                precipitation_rate = random.randrange(30)
            if precipitation_rate > 0:
                self._has_precipitation = True

            relative_humidity = None
            if "relative_humidity" in details:
                relative_humidity = details["relative_humidity"]

            wind_from_direction = None
            if "wind_from_direction" in details:
                wind_from_direction = details["wind_from_direction"]

            wind_speed = None
            if "wind_speed" in details:
                wind_speed = details["wind_speed"]

            wind_speed_of_gust = None
            if "wind_speed_of_gust" in details:
                wind_speed_of_gust = details["wind_speed_of_gust"]

            time = dt_util.parse_datetime(timeserie["time"])

            condition = None
            if "next_1_hours" in timeserie["data"]:
                condition = format_condition(
                    timeserie["data"]["next_1_hours"]["summary"]["symbol_code"]
                )

            if temp is not None:
                self._forecast.append(
                    Forecast(
                        temperature=temp,
                        precipitation=precipitation_rate,
                        relative_humidity=relative_humidity,
                        wind_bearing=wind_from_direction,
                        wind_speed=wind_speed,
                        wind_speed_of_gust=wind_speed_of_gust,
                        datetime=time,
                        condition=condition,
                    )
                )
            else:
                self._forecast.append(
                    Forecast(
                        temperature=temp,
                        precipitation=precipitation_rate,
                        datetime=time,
                    )
                )
        self._first_timeserie = self._raw_data["properties"]["timeseries"][0]
        _LOGGER.info(f"{self.location_name} updated")
