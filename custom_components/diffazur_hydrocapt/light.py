"""Platform for light integration."""
from __future__ import annotations

import logging


from .const import DOMAIN
from .entity import DiffazurHydrocaptEntity
from dataclasses import dataclass


# Import the device class from the component that you want to support
from homeassistant.components.light import (
    ATTR_BRIGHTNESS,
    PLATFORM_SCHEMA,
    LightEntity,
    LightEntityDescription,
)

_LOGGER = logging.getLogger(__name__)


@dataclass
class DiffazurHydrocaptLightEntityDescription(LightEntityDescription):
    """A class that describes Hidrocaptlight entity entities."""

    on_options: list[str] = None
    off_options: list[str] = None


async def async_setup_entry(hass, entry, async_add_devices):
    """Setup select platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    ext_cmds = coordinator.get_commands_and_options()
    lights = []
    for k_ext, cmds_val in ext_cmds.items():
        if "light" in k_ext:

            m = DiffazurHydrocaptLightEntityDescription(
                key=k_ext,
                name=f"pool_{k_ext}",
                on_options=["ON"],
                off_options=["OFF", "TIMER"],
            )

            s = DiffazurHydrocaptLightEntity(coordinator, m)

            lights.append(s)

    async_add_devices(lights)


class DiffazurHydrocaptLightEntity(DiffazurHydrocaptEntity, LightEntity):
    """diffazur_hydrocapt select class."""

    @property
    def unique_id(self):
        """Return a unique ID to use for this entity."""
        return f"HYDROCAPT-LightEntity-{self.entity_description.key}"

    @property
    def is_on(self) -> bool | None:
        """Return True if entity is on."""
        cur_op = self.coordinator.data[self.entity_description.key]
        ret = cur_op in self.entity_description.on_options

        if ret is False:
            self._prev_off_state = cur_op

        return ret

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the entity on."""
        self._prev_off_state, data = await self.hass.async_add_executor_job(
            self.coordinator.set_and_fetch_command_state,
            self.entity_description.key,
            self.entity_description.on_options[0],
        )
        # await self.coordinator.async_refresh()
        self.coordinator.async_set_updated_data(
            data
        )  # should be enough as set_and_fetch_command_state send back data

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the entity off."""

        if (
            self._prev_off_state is None
            or self._prev_off_state not in self.entity_description.off_options
        ):
            self._prev_off_state = self.entity_description.off_options[0]

        prev, data = await self.hass.async_add_executor_job(
            self.coordinator.set_and_fetch_command_state,
            self.entity_description.key,
            self._prev_off_state,
        )
        # await self.coordinator.async_refresh()
        self.coordinator.async_set_updated_data(
            data
        )  # should be enough as set_and_fetch_command_state send back data
