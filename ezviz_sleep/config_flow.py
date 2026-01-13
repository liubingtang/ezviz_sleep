"""Config flow for EZVIZ Sleep Companion integration."""
from __future__ import annotations

import logging
from typing import Any, Dict, Optional

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_NAME, CONF_API_KEY, CONF_DEVICE_ID
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult

from .api import EZVIZSleepCompanionAPI, EZVIZAPIError
from .const import (
    CONF_APP_KEY,
    CONF_APP_SECRET,
    CONF_DEVICE_SERIAL,
    CONF_DEVICE_NAME,
    DEFAULT_NAME,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)

# 配置步骤的选项
STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_APP_KEY): str,
        vol.Required(CONF_APP_SECRET): str,
        vol.Required(CONF_DEVICE_SERIAL): str,
        vol.Optional(CONF_DEVICE_NAME, default=DEFAULT_NAME): str,
    }
)

class EZVIZSleepCompanionConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for EZVIZ Sleep Companion."""
    
    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL
    
    def __init__(self) -> None:
        """Initialize the config flow."""
        self._data: Dict[str, Any] = {}
    
    async def async_step_user(self, user_input: Dict[str, Any] = None) -> FlowResult:
        """Handle the initial step."""
        errors: Dict[str, str] = {}
        
        if user_input is not None:
            try:
                # 验证凭据
                api = EZVIZSleepCompanionAPI(
                    self.hass,
                    app_key=user_input[CONF_APP_KEY],
                    app_secret=user_input[CONF_APP_SECRET],
                    device_serial=user_input[CONF_DEVICE_SERIAL],
                )
                
                # 测试连接
                await api.async_authenticate()
                
                # 保存数据
                self._data = user_input
                
                # 检查设备是否已配置
                await self.async_set_unique_id(user_input[CONF_DEVICE_SERIAL])
                self._abort_if_unique_id_configured()
                
                return self.async_create_entry(
                    title=user_input.get(CONF_DEVICE_NAME, DEFAULT_NAME),
                    data=user_input,
                )
                
            except EZVIZAPIError as err:
                _LOGGER.error("Unable to connect to EZVIZ API: %s", err)
                errors["base"] = "cannot_connect"
            except Exception as err:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception: %s", err)
                errors["base"] = "unknown"
        
        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
        )
    
    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> EZVIZSleepCompanionOptionsFlow:
        """Get the options flow for this handler."""
        return EZVIZSleepCompanionOptionsFlow(config_entry)


class EZVIZSleepCompanionOptionsFlow(config_entries.OptionsFlow):
    """Handle options flow for EZVIZ Sleep Companion."""
    
    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry
    
    async def async_step_init(
        self, user_input: Dict[str, Any] | None = None
    ) -> Dict[str, Any]:
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)
        
        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        "update_interval",
                        default=self.config_entry.options.get("update_interval", 300),
                    ): vol.All(vol.Coerce(int), vol.Range(min=60, max=3600)),
                }
            ),
        )
