"""萤石云无感睡眠伴侣传感器平台."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import PERCENTAGE, UnitOfTime
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

from .const import (
    ATTR_BREATH_RATE,
    ATTR_DEVICE_NAME,
    ATTR_DEVICE_SERIAL,
    ATTR_HEART_RATE,
    ATTR_SLEEP_STATUS,
    ATTR_BODY_MOVEMENT,
    ATTR_SLEEP_SCORE,
    ATTR_DEEP_SLEEP,
    ATTR_LIGHT_SLEEP,
    ATTR_AWAKE_TIME,
    CONF_ENABLE_HEART_RATE,
    CONF_ENABLE_BREATH_RATE,
    CONF_ENABLE_SLEEP_STATUS,
    CONF_ENABLE_BODY_MOVEMENT,
    CONF_ENABLE_SLEEP_SCORE,
    CONF_ENABLE_SLEEP_DURATION,
    DOMAIN,
    SLEEP_STATUS_MAP,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """设置萤石云睡眠伴侣传感器."""
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]

    entities = []
    for device_serial, device_data in coordinator.data.items():
        device_info = device_data["device_info"]
        device_name = device_info.get("deviceName", f"睡眠伴侣 {device_serial}")

        sensor_configs = []
        
        if entry.options.get(CONF_ENABLE_HEART_RATE, True):
            sensor_configs.append(
                ("heart_rate", "心率", "mdi:heart-pulse", "bpm", SensorDeviceClass.HEART_RATE)
            )
        
        if entry.options.get(CONF_ENABLE_BREATH_RATE, True):
            sensor_configs.append(
                ("breath_rate", "呼吸率", "mdi:lungs", "次/分", None)
            )
        
        if entry.options.get(CONF_ENABLE_SLEEP_STATUS, True):
            sensor_configs.append(
                ("sleep_status", "睡眠状态", "mdi:sleep", None, None)
            )
        
        if entry.options.get(CONF_ENABLE_BODY_MOVEMENT, True):
            sensor_configs.append(
                ("body_movement", "体动", "mdi:motion-sensor", None, None)
            )
        
        if entry.options.get(CONF_ENABLE_SLEEP_SCORE, True):
            sensor_configs.append(
                ("sleep_score", "睡眠评分", "mdi:star", None, None)
            )
        
        if entry.options.get(CONF_ENABLE_SLEEP_DURATION, True):
            sensor_configs.extend([
                ("deep_sleep", "深睡时长", "mdi:sleep", UnitOfTime.MINUTES, SensorDeviceClass.DURATION),
                ("light_sleep", "浅睡时长", "mdi:sleep", UnitOfTime.MINUTES, SensorDeviceClass.DURATION),
                ("awake_time", "清醒时长", "mdi:eye", UnitOfTime.MINUTES, SensorDeviceClass.DURATION),
            ])

        for sensor_type, sensor_name, icon, unit, device_class in sensor_configs:
            entities.append(
                EzvizSleepSensor(
                    coordinator,
                    device_serial,
                    device_name,
                    sensor_type,
                    sensor_name,
                    icon,
                    unit,
                    device_class,
                )
            )

    async_add_entities(entities)


class EzvizSleepSensor(CoordinatorEntity, SensorEntity):
    """萤石云睡眠伴侣传感器."""

    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        device_serial: str,
        device_name: str,
        sensor_type: str,
        sensor_name: str,
        icon: str,
        unit: str | None,
        device_class: SensorDeviceClass | None,
    ) -> None:
        """初始化传感器."""
        super().__init__(coordinator)
        self._device_serial = device_serial
        self._device_name = device_name
        self._sensor_type = sensor_type
        self._sensor_name = sensor_name
        self._icon = icon
        self._attr_native_unit_of_measurement = unit
        self._attr_device_class = device_class
        self._attr_state_class = (
            SensorStateClass.MEASUREMENT
            if sensor_type in ["heart_rate", "breath_rate"]
            else None
        )

        self._attr_unique_id = f"{device_serial}_{sensor_type}"
        self._attr_name = f"{device_name} {sensor_name}"

    @property
    def device_info(self) -> dict[str, Any]:
        """返回设备信息."""
        return {
            "identifiers": {(DOMAIN, self._device_serial)},
            "name": self._device_name,
            "manufacturer": "萤石云",
            "model": "无感睡眠伴侣",
        }

    @property
    def icon(self) -> str:
        """返回图标."""
        return self._icon

    @property
    def native_value(self) -> Any:
        """返回传感器状态."""
        if self._device_serial not in self.coordinator.data:
            return None

        sleep_data = self.coordinator.data[self._device_serial].get("sleep_data", {})

        if self._sensor_type == "heart_rate":
            return sleep_data.get(ATTR_HEART_RATE)
        elif self._sensor_type == "breath_rate":
            return sleep_data.get(ATTR_BREATH_RATE)
        elif self._sensor_type == "sleep_status":
            status_code = sleep_data.get(ATTR_SLEEP_STATUS)
            return SLEEP_STATUS_MAP.get(status_code, "未知")
        elif self._sensor_type == "body_movement":
            return sleep_data.get(ATTR_BODY_MOVEMENT)
        elif self._sensor_type == "sleep_score":
            return sleep_data.get(ATTR_SLEEP_SCORE)
        elif self._sensor_type == "deep_sleep":
            return sleep_data.get(ATTR_DEEP_SLEEP)
        elif self._sensor_type == "light_sleep":
            return sleep_data.get(ATTR_LIGHT_SLEEP)
        elif self._sensor_type == "awake_time":
            return sleep_data.get(ATTR_AWAKE_TIME)

        return None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """返回额外的状态属性."""
        if self._device_serial not in self.coordinator.data:
            return {}

        device_data = self.coordinator.data[self._device_serial]
        device_info = device_data.get("device_info", {})

        return {
            ATTR_DEVICE_SERIAL: self._device_serial,
            ATTR_DEVICE_NAME: self._device_name,
            "device_status": device_info.get("status"),
            "device_version": device_info.get("deviceVersion"),
        }
