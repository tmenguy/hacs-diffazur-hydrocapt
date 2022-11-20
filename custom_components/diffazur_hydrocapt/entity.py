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
        self._prev_off_state = None

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self.unique_id)},
            "name": f"{NAME} {self.entity_description.key}",
            "model": VERSION,
            "manufacturer": MANUFACTURER,
        }

    # @property
    # def extra_state_attributes(self):
    #     """Return the state attributes."""
    #     return {
    #         "attribution": ATTRIBUTION,
    #         "id": str(self.coordinator.data.get("id")),
    #         "integration": DOMAIN,
    #     }
