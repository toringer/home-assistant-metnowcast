from datetime import timedelta
import logging
import async_timeout

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .met_api import MetApi

_LOGGER = logging.getLogger(__name__)


class MetCoordinator(DataUpdateCoordinator):
    """Met coordinator."""

    def __init__(self, hass, config_entry, name, lat, long, met_api):
        """Initialize my coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            # Name of the data. For logging purposes.
            name=name,
            config_entry=config_entry,
            # Polling interval. Will only be polled if there are subscribers.
            update_interval=timedelta(minutes=7),
        )
        self._metApi = met_api
        self.lat = lat
        self.long = long


    async def _async_update_data(self):
        """Fetch data from API endpoint."""

        try:
            # Note: asyncio.TimeoutError and aiohttp.ClientError are already
            # handled by the data update coordinator.
            async with async_timeout.timeout(10):
                _LOGGER.debug(f"Fetching data from {self.lat}, {self.long}")
                return await self._metApi.get_now_cast(self.lat, self.long)
        except Exception as err:
            raise UpdateFailed(f"Error communicating with Met.no: {err}")

