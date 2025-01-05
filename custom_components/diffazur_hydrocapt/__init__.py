"""
Custom integration to integrate Diffazur Hydrocapt with Home Assistant.

For more details about this integration, please refer to
https://github.com/tmenguy/hacs-diffazur-hydrocapt
"""
import asyncio
import copy
from datetime import timedelta
import logging

try:
    from diffazur_hydrocapt.hydrocapt_lib.client import HydrocaptClient
except:
    from .hydrocapt_lib.client import HydrocaptClient


from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.core_config import Config
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.const import CONF_EMAIL, CONF_PASSWORD


from .const import (
    PLATFORMS,
    DOMAIN,
    STARTUP_MESSAGE,
    CONF_POOL_ID,
    CONF_INTERNAL_POOL_ID
)


SCAN_INTERVAL = timedelta(minutes=60)

_LOGGER: logging.Logger = logging.getLogger(__package__)


async def async_setup(hass: HomeAssistant, config: Config):
    """Set up this integration using YAML is not supported."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up this integration using UI."""
    if hass.data.get(DOMAIN) is None:
        hass.data.setdefault(DOMAIN, {})
        _LOGGER.info(STARTUP_MESSAGE)

    username = entry.data.get(CONF_EMAIL)
    password = entry.data.get(CONF_PASSWORD)
    pool_id = entry.data.get(CONF_POOL_ID, -1)
    pool_internal_id  = entry.data.get(CONF_INTERNAL_POOL_ID, -1)

    client = HydrocaptClient(username=username, password=password, pool_id=pool_id, pool_internal_id=pool_internal_id)

    coordinator = DiffazurHydrocaptDataUpdateCoordinator(hass, client)

    try:
        await coordinator.async_refresh()
    except:
        raise ConfigEntryNotReady

    if not coordinator.last_update_success:
        raise ConfigEntryNotReady

    hass.data[DOMAIN][entry.entry_id] = coordinator

    for platform in PLATFORMS:
        if entry.options.get(platform, True):
            coordinator.platforms.append(platform)

    await hass.config_entries.async_forward_entry_setups(
        entry, coordinator.platforms
    )

    entry.async_on_unload(entry.add_update_listener(async_reload_entry))
    return True


class DiffazurHydrocaptDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

    def __init__(
        self,
        hass: HomeAssistant,
        client: HydrocaptClient,
    ) -> None:
        """Initialize."""
        self.api = client
        self.platforms = []
        super().__init__(hass, _LOGGER, name=DOMAIN, update_interval=SCAN_INTERVAL)


    def get_pool_id(self):
        return self.api.get_pool_id()

    def set_command_state(self, command, state):
        self.api.set_command_state(command, state)
        data = self.api.get_packaged_data()
        self.data = data
        return data

    def set_consign(self, consign, value):
        self.api.set_consign(consign, value)
        data = self.api.get_packaged_data()
        self.data = data
        return data

    def set_consign_timer_hour(self, consign, hour_idx, value):
        self.api.set_consign_timer_hour(consign, hour_idx, value)
        data = self.api.get_packaged_data()
        self.data = data
        return data

    def set_and_fetch_command_state(self, command, state):
        prev_state = self.api.set_command_state(command, state, get_prev=True)
        data = self.api.get_packaged_data()
        self.data = data
        return prev_state, data

    def get_commands_and_options(self):
        return self.api.get_commands_and_options()

    def get_timers(self):
        return self.api.get_timers()


    def get_heating_regulation_command(self):
        return self.api.get_heating_regulation_command()

    def get_heating_regulation_temperature_consign(self):
        return self.api.get_heating_regulation_temperature_consign()

    def get_heating_regulation_water_temperature(self):
        return self.api.get_heating_regulation_water_temperature()

    async def _async_update_data(self):
        """Fetch data from API endpoint."""
        try:
            # id = await self.hass.async_add_executor_job(self.api._get_pool_internal_id)
            data = await self.hass.async_add_executor_job(self.api.fetch_all_data)
        except Exception as exception:
            raise UpdateFailed() from exception

        # data is the "new value" just remove None values from it to keep the old value
        if self.data is not None:
            new_data = copy.deepcopy(self.data)
        else:
            new_data = {}


        for k, v in data.items():
            if v is not None:
                new_data[k] = v

        return data


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Handle removal of an entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    unloaded = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, platform)
                for platform in PLATFORMS
                if platform in coordinator.platforms
            ]
        )
    )
    if unloaded:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unloaded


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
