"""DiffazurHydrocaptEntity class"""
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity import DeviceInfo, EntityDescription
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)

from homeassistant.util import dt as dt_util, ensure_unique_string, slugify

from .const import DOMAIN, NAME, VERSION, ATTRIBUTION, MANUFACTURER


class DiffazurHydrocaptEntity(CoordinatorEntity):

    _attr_attribution = ATTRIBUTION
    def __init__(self, coordinator: DataUpdateCoordinator, description: EntityDescription):
        super().__init__(coordinator)
        self.entity_description  = description

    @property
    def device_info(self):
        pool_id = self.coordinator.get_pool_id()
        return {
            "identifiers": {(DOMAIN, pool_id)},
            "name": f"{NAME} (pool id: {pool_id})",
            "model": VERSION,
            "manufacturer": MANUFACTURER,
        }

    @property
    def unique_id(self) -> str:
        """Return unique id for car entity."""
        pool_id = self.coordinator.get_pool_id()
        return slugify(f"{self.entity_description.name} {type(self).__name__} {pool_id}")


    # @property
    # def extra_state_attributes(self):
    #     """Return the state attributes."""
    #     return {
    #         "attribution": ATTRIBUTION,
    #         "id": str(self.coordinator.data.get("id")),
    #         "integration": DOMAIN,
    #     }
