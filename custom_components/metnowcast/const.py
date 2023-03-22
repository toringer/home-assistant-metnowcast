"""Constants for the met nowcast integration."""
from homeassistant.exceptions import HomeAssistantError
from homeassistant.components.weather import (
    ATTR_CONDITION_CLEAR_NIGHT,
    ATTR_CONDITION_CLOUDY,
    ATTR_CONDITION_FOG,
    ATTR_CONDITION_LIGHTNING_RAINY,
    ATTR_CONDITION_PARTLYCLOUDY,
    ATTR_CONDITION_POURING,
    ATTR_CONDITION_RAINY,
    ATTR_CONDITION_SNOWY,
    ATTR_CONDITION_SNOWY_RAINY,
    ATTR_CONDITION_SUNNY,
)

DOMAIN = "metnowcast"
NAME = "Met.no Nowcast"
ATTRIBUTION = (
    "Weather forecast from met.no, delivered by the Norwegian "
    "Meteorological Institute."
)
ATTR_RADAR_COVERAGE = "radar_coverage"
ATTR_RADAR_ONLINE = "radar_online"
ATTR_HAS_PRECIPITATION = "has_precipitation"
CONDITIONS_MAP = {
    ATTR_CONDITION_CLEAR_NIGHT: {"clearsky_night"},
    ATTR_CONDITION_CLOUDY: {"cloudy_night", "cloudy_day", "cloudy"},
    ATTR_CONDITION_FOG: {"fog", "fog_day", "fog_night"},
    ATTR_CONDITION_LIGHTNING_RAINY: {
        "heavyrainandthunder",
        "heavyrainandthunder_day",
        "heavyrainandthunder_night",
        "heavyrainshowersandthunder",
        "heavyrainshowersandthunder_day",
        "heavyrainshowersandthunder_night",
        "heavysleetandthunder",
        "heavysleetandthunder_day",
        "heavysleetandthunder_night",
        "heavysleetshowersandthunder",
        "heavysleetshowersandthunder_day",
        "heavysleetshowersandthunder_night",
        "heavysnowandthunder",
        "heavysnowandthunder_day",
        "heavysnowandthunder_night",
        "heavysnowshowersandthunder",
        "heavysnowshowersandthunder_day",
        "heavysnowshowersandthunder_night",
        "lightrainandthunder",
        "lightrainandthunder_day",
        "lightrainandthunder_night",
        "lightrainshowersandthunder",
        "lightrainshowersandthunder_day",
        "lightrainshowersandthunder_night",
        "lightsleetandthunder",
        "lightsleetandthunder_day",
        "lightsleetandthunder_night",
        "lightsnowandthunder",
        "lightsnowandthunder_day",
        "lightsnowandthunder_night",
        "lightssleetshowersandthunder",
        "lightssleetshowersandthunder_day",
        "lightssleetshowersandthunder_night",
        "lightssnowshowersandthunder",
        "lightssnowshowersandthunder_day",
        "lightssnowshowersandthunder_night",
        "rainandthunder",
        "rainandthunder_day",
        "rainandthunder_night",
        "rainshowersandthunder",
        "rainshowersandthunder_day",
        "rainshowersandthunder_night",
        "sleetandthunder",
        "sleetandthunder_day",
        "sleetandthunder_night",
        "sleetshowersandthunder",
        "sleetshowersandthunder_day",
        "sleetshowersandthunder_night",
        "snowshowersandthunder",
        "snowshowersandthunder_day",
        "snowshowersandthunder_night",
    },
    ATTR_CONDITION_PARTLYCLOUDY: {
        "fair",
        "fair_day",
        "fair_night",
        "partlycloudy",
        "partlycloudy_day",
        "partlycloudy_night",
    },
    ATTR_CONDITION_POURING: {
        "heavyrain",
        "heavyrain_day",
        "heavyrain_night",
        "heavyrainshowers",
        "heavyrainshowers_day",
        "heavyrainshowers_night",
    },
    ATTR_CONDITION_RAINY: {
        "lightrain",
        "lightrain_day",
        "lightrain_night",
        "lightrainshowers",
        "lightrainshowers_day",
        "lightrainshowers_night",
        "rain",
        "rain_day",
        "rain_night",
        "rainshowers",
        "rainshowers_day",
        "rainshowers_night",
    },
    ATTR_CONDITION_SNOWY: {
        "heavysnow",
        "heavysnow_day",
        "heavysnow_night",
        "heavysnowshowers",
        "heavysnowshowers_day",
        "heavysnowshowers_night",
        "lightsnow",
        "lightsnow_day",
        "lightsnow_night",
        "lightsnowshowers",
        "lightsnowshowers_day",
        "lightsnowshowers_night",
        "snow",
        "snow_day",
        "snow_night",
        "snowandthunder",
        "snowandthunder_day",
        "snowandthunder_night",
        "snowshowers",
        "snowshowers_day",
        "snowshowers_night",
    },
    ATTR_CONDITION_SNOWY_RAINY: {
        "heavysleet",
        "heavysleet_day",
        "heavysleet_night",
        "heavysleetshowers",
        "heavysleetshowers_day",
        "heavysleetshowers_night",
        "lightsleet",
        "lightsleet_day",
        "lightsleet_night",
        "lightsleetshowers",
        "lightsleetshowers_day",
        "lightsleetshowers_night",
        "sleet",
        "sleet_day",
        "sleet_night",
        "sleetshowers",
        "sleetshowers_day",
        "sleetshowers_night",
    },
    ATTR_CONDITION_SUNNY: {"clearsky_day", "clearsky"},
}


class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth."""


class NotFound(HomeAssistantError):
    """Error to indicate we cannot find weatcher information for the coordinate."""


class NoCoverage(HomeAssistantError):
    """No radar coverage."""
