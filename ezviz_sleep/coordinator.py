"""Data update coordinator for EZVIZ Sleep Companion."""
from __future__ import annotations

import asyncio
from datetime import timedelta
import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import EZVIZSleepCompanionAPI
from .const import (
    ATTR_BED_TIME,
    ATTR_BREATHING_RATE,
    ATTR_DEEP_SLEEP_DURATION,
    ATTR_DEVICE_MODEL,
    ATTR_HEART_RATE,
    ATTR_LAST_UPDATE,
    ATTR_LIGHT_SLEEP_DURATION,
    ATTR_SLEEP_DURATION,
    ATTR_SLEEP_EFFICIENCY,
    ATTR_SLEEP_SCORE,
    ATTR_SLEEP_STATE,
    ATTR_SOFTWARE_VERSION,
    ATTR_WAKE_UP_TIME,
    DEFAULT_UPDATE_INTERVAL,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)

class EZVIZSleepCompanionDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the EZVIZ Sleep Companion API."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize global EZVIZ Sleep Companion data updater."""
        self.api = EZVIZSleepCompanionAPI(
            hass=hass,
            app_key=entry.data["app_key"],
            app_secret=entry.data["app_secret"],
            device_serial=entry.data["device_serial"],
        )
        
        self.entry = entry
        update_interval = timedelta(seconds=entry.options.get("update_interval", DEFAULT_UPDATE_INTERVAL))
        
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=update_interval,
        )
    
    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from API endpoint."""
        try:
            # 获取设备信息
            device_info = await self.api.async_get_device_info()
            
            # 获取睡眠数据
            sleep_data = await self.api.async_get_sleep_data()
            
            # 合并数据
            data = {
                **device_info,
                **sleep_data,
                ATTR_LAST_UPDATE: device_info.get("last_update"),
            }
            
            _LOGGER.debug("Fetched new sleep data: %s", data)
            return data
            
        except Exception as err:
            _LOGGER.error("Error communicating with EZVIZ API: %s", err)
            raise UpdateFailed(f"Error communicating with EZVIZ API: {err}") from err
