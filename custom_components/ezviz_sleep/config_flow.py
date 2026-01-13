"""萤石云无感睡眠伴侣配置流程."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult

from .const import (
    CONF_APP_KEY,
    CONF_APP_SECRET,
    CONF_ENABLE_HEART_RATE,
    CONF_ENABLE_BREATH_RATE,
    CONF_ENABLE_SLEEP_STATUS,
    CONF_ENABLE_BODY_MOVEMENT,
    CONF_ENABLE_SLEEP_SCORE,
    CONF_ENABLE_SLEEP_DURATION,
    DOMAIN,
)
from .ezviz_api import EzvizSleepAPI

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_USERNAME): str,
        vol.Required(CONF_PASSWORD): str,
        vol.Optional(CONF_APP_KEY): str,
        vol.Optional(CONF_APP_SECRET): str,
    }
)


class EzvizSleepConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """处理萤石云睡眠伴侣的配置流程."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """处理用户配置步骤."""
        errors: dict[str, str] = {}

        if user_input is not None:
            username = user_input[CONF_USERNAME]
            password = user_input[CONF_PASSWORD]

            api = EzvizSleepAPI(
                username,
                password,
                user_input.get(CONF_APP_KEY),
                user_input.get(CONF_APP_SECRET),
            )

            try:
                await self.hass.async_add_executor_job(api.login)
            except Exception as err:
                _LOGGER.error("无法连接到萤石云: %s", err)
                errors["base"] = "cannot_connect"
            else:
                await self.async_set_unique_id(username)
                self._abort_if_unique_id_configured()

                return self.async_create_entry(
                    title=f"萤石云睡眠伴侣 ({username})",
                    data=user_input,
                )

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> EzvizSleepOptionsFlow:
        """获取选项流程."""
        return EzvizSleepOptionsFlow(config_entry)


class EzvizSleepOptionsFlow(config_entries.OptionsFlow):
    """处理萤石云睡眠伴侣的选项流程."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """初始化选项流程."""
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """管理选项."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        options_schema = vol.Schema(
            {
                vol.Optional(
                    CONF_ENABLE_HEART_RATE,
                    default=self.config_entry.options.get(CONF_ENABLE_HEART_RATE, True),
                ): bool,
                vol.Optional(
                    CONF_ENABLE_BREATH_RATE,
                    default=self.config_entry.options.get(CONF_ENABLE_BREATH_RATE, True),
                ): bool,
                vol.Optional(
                    CONF_ENABLE_SLEEP_STATUS,
                    default=self.config_entry.options.get(CONF_ENABLE_SLEEP_STATUS, True),
                ): bool,
                vol.Optional(
                    CONF_ENABLE_BODY_MOVEMENT,
                    default=self.config_entry.options.get(CONF_ENABLE_BODY_MOVEMENT, True),
                ): bool,
                vol.Optional(
                    CONF_ENABLE_SLEEP_SCORE,
                    default=self.config_entry.options.get(CONF_ENABLE_SLEEP_SCORE, True),
                ): bool,
                vol.Optional(
                    CONF_ENABLE_SLEEP_DURATION,
                    default=self.config_entry.options.get(CONF_ENABLE_SLEEP_DURATION, True),
                ): bool,
            }
        )

        return self.async_show_form(step_id="init", data_schema=options_schema)
