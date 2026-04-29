from __future__ import annotations
import voluptuous as vol
from homeassistant import config_entries

from .const import DOMAIN, CONF_ZIPCODE, CONF_HOUSE_NUMBER

class CleanProfsConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    # UI-drive setup flow (Settings -> Devices & Services -> Add integration).
    VERSION = 1

    # Ask the user for zipcode + house number, and create config entry
    async def async_step_user(self, user_input=None):
        # Enforce a single instance of this integration
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")
        
        if user_input is None:
            schema = vol.Schema({
                vol.Required(CONF_ZIPCODE): str,
                vol.Required(CONF_HOUSE_NUMBER): vol.Coerce(str)
            })
            return self.async_show_form(step_id="user", data_schema= schema)
        
        zipCode = user_input[CONF_ZIPCODE].strip()
        houseNumber = user_input[CONF_HOUSE_NUMBER].strip()

        # Use a fixed unique id so Home Assistant van detect duplicates
        await self.async_set_unique_id("cleanprofs_single_instance")
        self._abort_if_unique_id_configured()

        return self.async_create_entry(
            title="CleanProfs",
            data={CONF_ZIPCODE: zipCode, CONF_HOUSE_NUMBER: houseNumber}
        )