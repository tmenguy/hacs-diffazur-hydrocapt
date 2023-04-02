"""Binary sensor platform for Diffazur Hydrocapt."""
from homeassistant.components.binary_sensor import BinarySensorEntity


from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)


from .const import (
    DOMAIN, PREFIX
)
from .entity import DiffazurHydrocaptEntity




BINARY_SENSORS_TYPES: tuple[BinarySensorEntityDescription, ...] = (
    BinarySensorEntityDescription(
        key="ph_status",
        name=f"{PREFIX} pH Status",
        device_class=BinarySensorDeviceClass.PROBLEM,
    ),
    BinarySensorEntityDescription(
        key="conductivity_status",
        name=f"{PREFIX} Conductivity Status",
        device_class=BinarySensorDeviceClass.PROBLEM,
    ),
    BinarySensorEntityDescription(
        key="redox_status",
        name=f"{PREFIX} Redox (ORP) Status",
        device_class=BinarySensorDeviceClass.PROBLEM,
    ),
)



async def async_setup_entry(hass, entry, async_add_devices):
    """Setup binary_sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_devices(
        DiffazurHydrocaptBinarySensor(coordinator, description)
        for description in BINARY_SENSORS_TYPES
    )


class DiffazurHydrocaptBinarySensor(DiffazurHydrocaptEntity, BinarySensorEntity):
    """diffazur_hydrocapt binary_sensor class."""

    @property
    def is_on(self):
        """Return true if the binary sensor is on in case of a Problem is detected."""
        if self.coordinator.data is None:
            return None
        if self.coordinator.data.get(self.entity_description.key, None) is None:
            return None

        return (
            self.coordinator.data[self.entity_description.key] == "TooLow"
            or self.coordinator.data[self.entity_description.key] == "TooHigh"
        )
