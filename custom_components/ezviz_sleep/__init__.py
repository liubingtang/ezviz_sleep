"""萤石云无感睡眠伴侣集成."""
from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME, Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN
from .ezviz_api import EzvizSleepAPI

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SENSOR]

SCAN_INTERVAL = timedelta(minutes=5)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """设置萤石云睡眠伴侣集成."""
    username = entry.data[CONF_USERNAME]
    password = entry.data[CONF_PASSWORD]

    api = EzvizSleepAPI(username, password)

    try:
        await hass.async_add_executor_job(api.login)
    except Exception as err:
        _LOGGER.error("无法连接到萤石云API: %s", err)
        raise ConfigEntryNotReady from err

    async def async_update_data():
        """从API获取数据."""
        try:
            devices = await hass.async_add_executor_job(api.get_sleep_devices)
            data = {}
            for device in devices:
                device_serial = device.get("deviceSerial")
                if device_serial:
                    sleep_data = await hass.async_add_executor_job(
                        api.get_sleep_data, device_serial
                    )
                    data[device_serial] = {
                        "device_info": device,
                        "sleep_data": sleep_data,
                    }
            return data
        except Exception as err:
            raise UpdateFailed(f"更新数据失败: {err}") from err

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name=DOMAIN,
        update_method=async_update_data,
        update_interval=SCAN_INTERVAL,
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        "api": api,
        "coordinator": coordinator,
    }

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    return True


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """重新加载配置条目."""
    await hass.config_entries.async_reload(entry.entry_id)


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """卸载萤石云睡眠伴侣集成."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
