from homeassistant.components.switch import SwitchEntity
from homeassistant.components.switch import SwitchEntityDescription


from .const import DOMAIN, PREFIX
from .entity import DiffazurHydrocaptEntity
from dataclasses import dataclass


@dataclass
class DiffazurHydrocapSwitchEntityDescription(SwitchEntityDescription):
    option_on: str = None
    option_off: str = None


@dataclass
class DiffazurHydrocapSwitchHourTimerEntityDescription(SwitchEntityDescription):
    hour_idx: str = 0


async def async_setup_entry(hass, entry, async_add_devices):
    """Setup select platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    selects = []
    ext_cmds = coordinator.get_commands_and_options()
    for k_ext, cmd_vals in ext_cmds.items():

        #do not expose hesting command here as we do have now a climate entity for that
        if k_ext == coordinator.get_heating_regulation_command():
            continue

        if len(cmd_vals) == 2:

            #by construction first command is off
            m = DiffazurHydrocapSwitchEntityDescription(
                key=k_ext,
                name=f"{PREFIX} {k_ext} Switch",
                icon="mdi:pool",
                option_on=cmd_vals[1],
                option_off=cmd_vals[0],
            )

            s = DiffazurHydrocaptSwitchEntity(coordinator, m)

            selects.append(s)

    timers = coordinator.get_timers()
    for timer_name, timer_pre in timers.items():

        for hour_idx in range(24):

            if hour_idx < 10:
                idx_str = "0" + str(hour_idx)
            else:
                idx_str = str(hour_idx)

            m = DiffazurHydrocapSwitchHourTimerEntityDescription(
                key=timer_name,
                name=f"{PREFIX} {timer_pre}{idx_str}h",
                hour_idx=hour_idx,
            )

            s = DiffazurHydrocapSwitchHourTimerEntity(coordinator, m)

            selects.append(s)

    async_add_devices(selects)


class DiffazurHydrocaptSwitchEntity(DiffazurHydrocaptEntity, SwitchEntity):
    """integration_blueprint switch class."""

    async def async_turn_on(self, **kwargs):  # pylint: disable=unused-argument
        """Turn on the switch."""
        data = await self.hass.async_add_executor_job(
            self.coordinator.set_command_state,
            self.entity_description.key,
            self.entity_description.option_on,
        )
        # await self.coordinator.async_refresh()
        self.coordinator.async_set_updated_data(
            data
        )

    async def async_turn_off(self, **kwargs):  # pylint: disable=unused-argument
        """Turn off the switch."""
        data = await self.hass.async_add_executor_job(
            self.coordinator.set_command_state,
            self.entity_description.key,
            self.entity_description.option_off,
        )
        # await self.coordinator.async_refresh()
        self.coordinator.async_set_updated_data(
            data
        )

    @property
    def is_on(self):
        """Return true if the switch is on."""
        cur_op = self.coordinator.data[self.entity_description.key]
        ret = cur_op == self.entity_description.option_on
        return ret


class DiffazurHydrocapSwitchHourTimerEntity(DiffazurHydrocaptEntity, SwitchEntity):
    """integration_blueprint switch class."""

    async def async_turn_on(self, **kwargs):  # pylint: disable=unused-argument
        """Turn on the switch."""
        data = await self.hass.async_add_executor_job(
            self.coordinator.set_consign_timer_hour,
            self.entity_description.key,
            self.entity_description.hour_idx,
            True,
        )
        # await self.coordinator.async_refresh()
        self.coordinator.async_set_updated_data(
            data
        )

    async def async_turn_off(self, **kwargs):  # pylint: disable=unused-argument
        """Turn off the switch."""
        data = await self.hass.async_add_executor_job(
            self.coordinator.set_consign_timer_hour,
            self.entity_description.key,
            self.entity_description.hour_idx,
            False,
        )
        # await self.coordinator.async_refresh()
        self.coordinator.async_set_updated_data(
            data
        )

    @property
    def is_on(self):
        """Return true if the switch is on."""
        cur_timer = self.coordinator.data.get(self.entity_description.key)
        if cur_timer is not None:
            return cur_timer[self.entity_description.hour_idx]
        return False
