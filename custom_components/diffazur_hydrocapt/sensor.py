"""Sensor platform for Diffazur Hydrocapt."""

from .const import DOMAIN, PREFIX
from .entity import DiffazurHydrocaptEntity

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)

from homeassistant.const import ELECTRIC_POTENTIAL_MILLIVOLT, TEMP_CELSIUS



SENSOR_TYPES: tuple[SensorEntityDescription, ...] = (
    SensorEntityDescription(
        key="conductivity",
        name=f"{PREFIX} conductivity",
        native_unit_of_measurement=ELECTRIC_POTENTIAL_MILLIVOLT,
        icon="mdi:pool",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="ph",
        name=f"{PREFIX} pH",
        icon="mdi:pool",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="water_temperature",
        name=f"{PREFIX} Water Temp",
        icon="mdi:coolant-temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=TEMP_CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="technical_room_temperature",
        name=f"{PREFIX} Technical Room Temp",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=TEMP_CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="redox",
        name=f"{PREFIX} Redox (ORP)",
        native_unit_of_measurement=ELECTRIC_POTENTIAL_MILLIVOLT,
        icon="mdi:pool",
        state_class=SensorStateClass.MEASUREMENT,
    ),
)



async def async_setup_entry(hass, entry, async_add_devices):
    """Setup sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    sensors = [DiffazurHydrocaptSensor(coordinator, description) for description in SENSOR_TYPES]
    async_add_devices(sensors)


class DiffazurHydrocaptSensor(DiffazurHydrocaptEntity, SensorEntity):
    """diffazur_hydrocapt Sensor class."""

    @property
    def native_value(self):
        """State of the sensor."""
        if self.coordinator.data is None:
            return None
        return self.coordinator.data.get(self.entity_description.key, None)


