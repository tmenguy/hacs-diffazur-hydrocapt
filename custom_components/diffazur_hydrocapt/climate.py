from homeassistant.components.climate import ClimateEntity
from homeassistant.components.climate import ClimateEntityDescription

from .const import DOMAIN, PREFIX
from .entity import DiffazurHydrocaptEntity
from dataclasses import dataclass

from homeassistant.const import ATTR_TEMPERATURE

from homeassistant.components.climate.const import (
    HVACMode,
    ClimateEntityFeature,
)

from homeassistant.const import (
    UnitOfTemperature,
)

@dataclass
class DiffazurHydrocaptClimateEntityDescription(ClimateEntityDescription):
    """A class that describes climate entities."""

    heating_command: str = None
    water_temperature: str = None
    heating_setpoint: str = None


async def async_setup_entry(hass, entry, async_add_devices):
    """Setup select platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    selects = []

    m = DiffazurHydrocaptClimateEntityDescription(
        key="pool heater",
        name=f"{PREFIX} Heater",
        heating_command = coordinator.get_heating_regulation_command(),
        water_temperature = coordinator.get_heating_regulation_water_temperature(),
        heating_setpoint = coordinator.get_heating_regulation_temperature_consign()


    )

    s = DiffazurHydrocaptClimateEntity(coordinator, m)

    selects.append(s)

    async_add_devices(selects)

SUPPORT_HVAC = [HVACMode.AUTO, HVACMode.OFF]

class DiffazurHydrocaptClimateEntity(DiffazurHydrocaptEntity, ClimateEntity):

    _attr_hvac_modes = SUPPORT_HVAC
    _attr_supported_features = (
        ClimateEntityFeature.TARGET_TEMPERATURE
        | ClimateEntityFeature.TURN_OFF
        | ClimateEntityFeature.TURN_ON
    )
    _attr_temperature_unit = UnitOfTemperature.CELSIUS
    _attr_max_temp = 35
    _attr_min_temp = 5
    _enable_turn_on_off_backwards_compatibility = False

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
    def current_temperature(self):
        """Return current temperature."""
        return self.coordinator.data.get(self.entity_description.water_temperature, 0)



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
            )
