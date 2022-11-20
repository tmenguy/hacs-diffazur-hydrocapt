"""Select platform for Diffazur Hydrocapt."""

from .const import DOMAIN, PREFIX
from .entity import DiffazurHydrocaptEntity
from dataclasses import dataclass


from homeassistant.components.select import (
    SelectEntity,
    SelectEntityDescription,
)


@dataclass
class DiffazurHydrocapSelectEntityDescription(SelectEntityDescription):
    options: list[str] = None


async def async_setup_entry(hass, entry, async_add_devices):
    """Setup select platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    selects = []
    ext_cmds = coordinator.get_commands_and_options()
    for k_ext, cmd_vals in ext_cmds.items():

        if len(cmd_vals) > 2:
            m = DiffazurHydrocapSelectEntityDescription(
                key=k_ext, name=f"{PREFIX} {k_ext} Mode", icon="mdi:pool", options=cmd_vals
            )

            s = DiffazurHydrocaptSelectEntity(coordinator, m)

            selects.append(s)

    async_add_devices(selects)


class DiffazurHydrocaptSelectEntity(DiffazurHydrocaptEntity, SelectEntity):
    """diffazur_hydrocapt select class."""

    @property
    def options(self):
        return self.entity_description.options

    @property
    def current_option(self):
        """Return the selected entity option to represent the entity state."""
        if self.coordinator.data is None:
            return None
        return self.coordinator.data.get(self.entity_description.key, None)

    # def select_option(self, option: str) -> None:
    #    """Change the selected option. by construction the set_and_fetch_command_state will set the new data in the coordinator too"""
    #    self.coordinator.set_and_fetch_command_state(self.entity_description.key, option)

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        data = await self.hass.async_add_executor_job(
            self.coordinator.set_command_state,
            self.entity_description.key,
            option,
        )
        # await self.coordinator.async_refresh()
        await self.coordinator.async_set_updated_data(
            data
        )  # should be enough as set_and_fetch_command_state send back data
