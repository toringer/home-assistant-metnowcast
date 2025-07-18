"""met.no now cast component."""
from __future__ import annotations
import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.const import CONF_LATITUDE, CONF_LONGITUDE, CONF_NAME
from .const import DOMAIN
from .coordinator import MetCoordinator
import asyncio
from .met_api import MetApi

PLATFORMS: list[Platform] = [Platform.WEATHER]
_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Met.no Nowcast entry."""
    lat = entry.data[CONF_LATITUDE]
    lon = entry.data[CONF_LONGITUDE]
    name = entry.data[CONF_NAME]

    # Ensure DOMAIN is initialized in hass.data
    hass.data.setdefault(DOMAIN, {})
    # Create and store a single MetApi instance if not already present
    if "api" not in hass.data[DOMAIN]:
        hass.data[DOMAIN]["api"] = MetApi(hass)
    api = hass.data[DOMAIN]["api"]

    coordinator = MetCoordinator(hass, entry, name, lat, lon, api)
    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN][entry.entry_id] = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Handle removal of an entry."""
    _LOGGER.debug("async_unload_entry")

    unloaded = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, platform)
                for platform in PLATFORMS
            ]
        )
    )
    if unloaded:
        hass.data[DOMAIN].pop(entry.entry_id)
        _LOGGER.debug("pop coordinator")
    return unloaded


async def async_migrate_entry(hass, config_entry: ConfigEntry):
    """Migrate old entry."""
    _LOGGER.debug("Migrating configuration from version %s.%s", config_entry.version, config_entry.minor_version)

    if config_entry.version == 1:

        new_data = {**config_entry.data}

        new_data[CONF_LATITUDE] = round(new_data[CONF_LATITUDE],4)
        new_data[CONF_LONGITUDE] = round(new_data[CONF_LONGITUDE],4)

        hass.config_entries.async_update_entry(config_entry, data=new_data, minor_version=0, version=2)

    _LOGGER.debug("Migration to configuration version %s.%s successful", config_entry.version, config_entry.minor_version)

    return True