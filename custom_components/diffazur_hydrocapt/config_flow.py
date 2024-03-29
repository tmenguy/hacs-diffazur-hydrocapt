"""Adds config flow for Diffazur hydrocapt."""
from homeassistant import config_entries
from homeassistant.core import callback
import voluptuous as vol

from homeassistant.const import CONF_EMAIL, CONF_PASSWORD

try:
    from diffazur_hydrocapt.hydrocapt_lib.client import HydrocaptClient
except Exception:
    from .hydrocapt_lib.client import HydrocaptClient

from .const import DOMAIN, PLATFORMS, CONF_POOL_ID, CONF_INTERNAL_POOL_ID


class DiffazurHydrocaptFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for diffazur_hydrocapt."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    def __init__(self):
        """Initialize."""
        self._errors = {}

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        self._errors = {}

        # Uncomment the next 2 lines if only a single instance of the integration is allowed:
        # if self._async_current_entries():
        #     return self.async_abort(reason="single_instance_allowed")

        if user_input is not None:
            valid = await self._test_credentials(
                user_input[CONF_EMAIL],
                user_input[CONF_PASSWORD],
                user_input[CONF_POOL_ID],
                user_input[CONF_INTERNAL_POOL_ID],
            )
            if valid:
                return self.async_create_entry(
                    title=user_input[CONF_EMAIL], data=user_input
                )
            else:
                self._errors["base"] = "auth"

            return await self._show_config_form(user_input)

        user_input = {}
        # Provide defaults for form
        user_input[CONF_EMAIL] = ""
        user_input[CONF_PASSWORD] = ""
        user_input[CONF_POOL_ID] = -1
        user_input[CONF_INTERNAL_POOL_ID] = -1

        return await self._show_config_form(user_input)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return DiffazurHydrocaptOptionsFlowHandler(config_entry)

    async def _show_config_form(self, user_input):  # pylint: disable=unused-argument
        """Show the configuration form to edit location data."""
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_EMAIL, default=user_input[CONF_EMAIL]): str,
                    vol.Required(CONF_PASSWORD, default=user_input[CONF_PASSWORD]): str,
                    vol.Optional(CONF_POOL_ID, default=user_input[CONF_POOL_ID]): int,
                    vol.Optional(
                        CONF_INTERNAL_POOL_ID, default=user_input[CONF_INTERNAL_POOL_ID]
                    ): int,
                }
            ),
            errors=self._errors,
        )

    async def _test_credentials(self, username, password, pool_id, internal_pool_id):
        """Return true if credentials is valid."""
        try:
            client = HydrocaptClient(username, password, pool_id, internal_pool_id)
            conn_status = await self.hass.async_add_executor_job(
                client.is_connection_ok
            )
            return conn_status
        except Exception:
            pass

        return False


class DiffazurHydrocaptOptionsFlowHandler(config_entries.OptionsFlow):
    """Config flow options handler for diffazur_hydrocapt."""

    def __init__(self, config_entry):
        """Initialize HACS options flow."""
        self.config_entry = config_entry
        self.options = dict(config_entry.options)

    async def async_step_init(self, user_input=None):  # pylint: disable=unused-argument
        """Manage the options."""
        return await self.async_step_user()

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        if user_input is not None:
            self.options.update(user_input)
            return await self._update_options()

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(x, default=self.options.get(x, True)): bool
                    for x in sorted(PLATFORMS)
                }
            ),
        )

    async def _update_options(self):
        """Update config entry options."""
        return self.async_create_entry(
            title=self.config_entry.data.get(CONF_EMAIL), data=self.options
        )
