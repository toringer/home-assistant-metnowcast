"""met.no now cast component."""
from __future__ import annotations
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from .const import DOMAIN
from .met_api import MetApi

PLATFORMS: list[Platform] = [Platform.WEATHER]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Met.no Nowcast entry."""
    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = {}

    hass.config_entries.async_setup_platforms(entry, PLATFORMS)

    api = MetApi()
    hass.data[DOMAIN]["api"] = api
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN]["api"] = None
    return unload_ok
