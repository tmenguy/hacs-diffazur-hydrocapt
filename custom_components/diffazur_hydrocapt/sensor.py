"""Sensor platform for Diffazur Hydrocapt."""

from .const import DOMAIN
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
        name="conductivity",
        native_unit_of_measurement=ELECTRIC_POTENTIAL_MILLIVOLT,
        icon="mdi:pool",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="ph",
        name="pH",
        icon="mdi:pool",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="water_temperature",
        name="Water Temp",
        icon="mdi:coolant-temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=TEMP_CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="technical_room_temperature",
        name="Technical Room Temp",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=TEMP_CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="red_ox",
        name="Red OX",
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
        return self.coordinator.data[self.entity_description.key]


