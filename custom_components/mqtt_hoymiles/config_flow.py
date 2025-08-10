"""Integration config and option flow."""

from typing import Any

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback

from .const import DOMAIN, BasicConfig, ExtendedConfig

CONFIG_SCHEMA = vol.Schema(
    {
        vol.Required(BasicConfig.DTU_HOST.name): BasicConfig.DTU_HOST.type,
        vol.Optional(
            BasicConfig.DTU_PORT.name, default=BasicConfig.DTU_PORT.default
        ): BasicConfig.DTU_PORT.type,
        vol.Required(BasicConfig.MQTT_BROKER.name): BasicConfig.MQTT_BROKER.type,
        vol.Optional(
            BasicConfig.MQTT_PORT.name,
            default=BasicConfig.MQTT_PORT.default,
        ): BasicConfig.MQTT_PORT.type,
        vol.Optional(BasicConfig.MQTT_USER.name): BasicConfig.MQTT_USER.type,
        vol.Optional(BasicConfig.MQTT_PASSWORD.name): BasicConfig.MQTT_PASSWORD.type,
        vol.Optional(BasicConfig.MQTT_TLS.name): BasicConfig.MQTT_TLS.type,
        vol.Optional(
            BasicConfig.MQTT_TLS_INSECURE.name
        ): BasicConfig.MQTT_TLS_INSECURE.type,
    }
)


class HoymilesMqttHaIntegrationFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for the integration."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    def __init__(self) -> None:
        """Initialize."""
        self._errors = {}

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.ConfigFlowResult:
        """Handle a flow initialized by the user."""
        self._errors = {}

        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        if user_input is not None:
            return self.async_create_entry(
                title=f"DTU: {user_input[BasicConfig.DTU_HOST.name]}", data=user_input
            )

        return await self._show_config_form()

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> config_entries.OptionsFlow:
        """Get the options flow for this handler."""
        return HoymilesMqttHaIntegrationOptionsFlowHandler(config_entry)

    async def _show_config_form(self) -> config_entries.ConfigFlowResult:
        """Show the configuration form to edit location data."""
        return self.async_show_form(
            step_id="user",
            data_schema=CONFIG_SCHEMA,
            errors=self._errors,
        )


OPTIONS_SCHEMA = vol.Schema(
    {
        vol.Optional(
            ExtendedConfig.QUERY_PERIOD.name,
            default=ExtendedConfig.QUERY_PERIOD.default,
        ): ExtendedConfig.QUERY_PERIOD.type,
        vol.Optional(
            ExtendedConfig.MI_ENTITIES.name,
            default=ExtendedConfig.MI_ENTITIES.default,
        ): ExtendedConfig.MI_ENTITIES.type,
        vol.Optional(
            ExtendedConfig.PORT_ENTITIES.name,
            default=ExtendedConfig.PORT_ENTITIES.default,
        ): ExtendedConfig.PORT_ENTITIES.type,
        vol.Optional(
            ExtendedConfig.EXPIRE_AFTER.name,
            default=ExtendedConfig.EXPIRE_AFTER.default,
        ): ExtendedConfig.EXPIRE_AFTER.type,
        vol.Optional(
            ExtendedConfig.COMM_TIMEOUT.name,
            default=ExtendedConfig.COMM_TIMEOUT.default,
        ): ExtendedConfig.COMM_TIMEOUT.type,
        vol.Optional(
            ExtendedConfig.COMM_RETRIES.name,
            default=ExtendedConfig.COMM_RETRIES.default,
        ): ExtendedConfig.COMM_RETRIES.type,
        vol.Optional(
            ExtendedConfig.COMM_RECONNECT_DELAY.name,
            default=ExtendedConfig.COMM_RECONNECT_DELAY.default,
        ): ExtendedConfig.COMM_RECONNECT_DELAY.type,
        vol.Optional(
            ExtendedConfig.COMM_RECONNECT_DELAY_MAX.name,
            default=ExtendedConfig.COMM_RECONNECT_DELAY_MAX.default,
        ): ExtendedConfig.COMM_RECONNECT_DELAY_MAX.type,
    }
)


class HoymilesMqttHaIntegrationOptionsFlowHandler(config_entries.OptionsFlow):
    """Config flow options handler for the integration."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize HACS options flow."""
        self.config_entry = config_entry
        self.options = dict(config_entry.options)

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.ConfigFlowResult:
        """Manage the options."""
        if user_input is not None:
            self.options.update(user_input)
            return await self._update_options()

        return self.async_show_form(
            step_id="init",
            data_schema=self.add_suggested_values_to_schema(
                OPTIONS_SCHEMA, self.config_entry.options
            ),
        )

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.ConfigFlowResult:
        """Handle a flow initialized by the user."""
        if user_input is not None:
            self.options.update(user_input)
            return await self._update_options()

        return self.async_show_form(
            step_id="user",
            data_schema=self.add_suggested_values_to_schema(
                OPTIONS_SCHEMA, self.config_entry.options
            ),
        )

    async def _update_options(self) -> config_entries.ConfigFlowResult:
        """Update config entry options."""
        return self.async_create_entry(title="Additional options", data=self.options)
