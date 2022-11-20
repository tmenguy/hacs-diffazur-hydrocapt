from homeassistant.components.climate import ClimateEntity
from homeassistant.components.climate import ClimateEntityDescription

from .const import DOMAIN, PREFIX
from .entity import DiffazurHydrocaptEntity
from dataclasses import dataclass

from homeassistant.const import ATTR_TEMPERATURE, TEMP_CELSIUS

from homeassistant.components.climate.const import (
    HVACMode,
    ClimateEntityFeature,
)


@dataclass
class DiffazurHydrocaptClimateEntityDescription(ClimateEntityDescription):
    """A class that describes climate entities."""

    heating_command: str = "Heating Regulation"
    water_temperature: str = "water_temperature"
    heating_setpoint: str = "setpoint_heating"


async def async_setup_entry(hass, entry, async_add_devices):
    """Setup select platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    selects = []

    m = DiffazurHydrocaptClimateEntityDescription(
        key="pool heater", name=f"{PREFIX} Heater"
    )

    s = DiffazurHydrocaptClimateEntity(coordinator, m)

    selects.append(s)

    async_add_devices(selects)


class DiffazurHydrocaptClimateEntity(DiffazurHydrocaptEntity, ClimateEntity):
    @property
    def supported_features(self):
        """Return the list of supported features."""
        return ClimateEntityFeature.TARGET_TEMPERATURE

    @property
    def hvac_mode(self):
        """Return hvac operation ie. heat, cool mode.
        Need to be one of HVAC_MODE_*.
        """
        if (
            self.coordinator.data.get(
                self.entity_description.heating_command, "Pool Heat AUTO"
            )
            == "Pool Heat AUTO"
        ):
            return HVACMode.AUTO

        return HVACMode.OFF

    @property
    def hvac_modes(self):
        """Return list of available hvac operation modes.
        Need to be a subset of HVAC_MODES.
        """
        return [HVACMode.OFF, HVACMode.AUTO]

    @property
    def temperature_unit(self):
        """Return unit of measurement.
        Tesla API always returns in Celsius.
        """
        return TEMP_CELSIUS

    @property
    def current_temperature(self):
        """Return current temperature."""
        return self.coordinator.data.get(self.entity_description.water_temperature, 0)

    @property
    def max_temp(self):
        """Return max temperature."""
        return 35  # DEFAULT_MAX_TEMP

    @property
    def min_temp(self):
        """Return min temperature"""
        return 3  # DEFAULT_MIN_TEMP

    @property
    def target_temperature(self):
        """Return target temperature."""
        return self.coordinator.data.get(self.entity_description.heating_setpoint, 0)

    async def async_set_temperature(self, **kwargs):
        """Set new target temperature."""
        temperature = kwargs.get(ATTR_TEMPERATURE)
        if temperature:
            # _LOGGER.debug("%s: Setting temperature to %s", self.name, temperature)
            temp = round(temperature)

            data = await self.hass.async_add_executor_job(
                self.coordinator.set_consign,
                self.entity_description.heating_setpoint,
                temp,
            )
            # await self.coordinator.async_refresh()
            self.coordinator.async_set_updated_data(data)

            await self.async_update_ha_state()

    async def async_set_hvac_mode(self, hvac_mode):
        """Set new target hvac mode."""
        option = None

        if hvac_mode == HVACMode.OFF:
            option = "Pool Heat OFF"
        elif hvac_mode == HVACMode.AUTO:
            option = "Pool Heat AUTO"

        if option is not None:
            data = await self.hass.async_add_executor_job(
                self.coordinator.set_command_state,
                self.entity_description.heating_command,
                option
            )
            # await self.coordinator.async_refresh()
            self.coordinator.async_set_updated_data(
                data
            )  # should be enough as set_and_fetch_command_state send back data
