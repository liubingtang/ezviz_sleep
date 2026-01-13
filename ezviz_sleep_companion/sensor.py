"""Sensor platform for EZVIZ Sleep Companion."""
from __future__ import annotations

import logging
from typing import Any, Callable, Dict, Optional

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    PERCENTAGE,
    TIME_MINUTES,
    ATTR_ATTRIBUTION,
    ATTR_DEVICE_CLASS,
    ATTR_ICON,
    ATTR_NAME,
    ATTR_UNIT_OF_MEASUREMENT,
)
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType
from homeassistant.helpers.update_coordinator import CoordinatorEntity

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
    ATTRIBUTION,
    DEFAULT_NAME,
    DOMAIN,
    SENSOR_TYPES,
)
from .coordinator import EZVIZSleepCompanionDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

# 传感器类型与属性的映射
SENSOR_TYPE_MAP = {
    "sleep_score": {
        "attr": ATTR_SLEEP_SCORE,
        "unit": PERCENTAGE,
        "icon": "mdi:sleep",
        "name": "Sleep Score",
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
    },
    "heart_rate": {
        "attr": ATTR_HEART_RATE,
        "unit": "bpm",
        "icon": "mdi:heart-pulse",
        "name": "Heart Rate",
        "device_class": SensorDeviceClass.HEART_RATE,
        "state_class": SensorStateClass.MEASUREMENT,
    },
    "breathing_rate": {
        "attr": ATTR_BREATHING_RATE,
        "unit": "rpm",
        "icon": "mdi:weather-windy",
        "name": "Breathing Rate",
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
    },
    "sleep_duration": {
        "attr": ATTR_SLEEP_DURATION,
        "unit": TIME_MINUTES,
        "icon": "mdi:clock-time-eight-outline",
        "name": "Sleep Duration",
        "device_class": SensorDeviceClass.DURATION,
        "state_class": SensorStateClass.MEASUREMENT,
    },
    "deep_sleep_duration": {
        "attr": ATTR_DEEP_SLEEP_DURATION,
        "unit": TIME_MINUTES,
        "icon": "mdi:sleep",
        "name": "Deep Sleep Duration",
        "device_class": SensorDeviceClass.DURATION,
        "state_class": SensorStateClass.MEASUREMENT,
    },
    "light_sleep_duration": {
        "attr": ATTR_LIGHT_SLEEP_DURATION,
        "unit": TIME_MINUTES,
        "icon": "mdi:sleep-off",
        "name": "Light Sleep Duration",
        "device_class": SensorDeviceClass.DURATION,
        "state_class": SensorStateClass.MEASUREMENT,
    },
    "sleep_efficiency": {
        "attr": ATTR_SLEEP_EFFICIENCY,
        "unit": PERCENTAGE,
        "icon": "mdi:chart-arc",
        "name": "Sleep Efficiency",
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
    },
}


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up EZVIZ Sleep Companion sensors based on a config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    
    # 为每种传感器类型创建一个实体
    entities = [
        EZVIZSleepCompanionSensor(coordinator, sensor_type, entry)
        for sensor_type in SENSOR_TYPE_MAP
    ]
    
    async_add_entities(entities, True)


class EZVIZSleepCompanionSensor(
    CoordinatorEntity[EZVIZSleepCompanionDataUpdateCoordinator], SensorEntity
):
    """Representation of an EZVIZ Sleep Companion sensor."""

    _attr_has_entity_name = True
    _attr_should_poll = False

    def __init__(
        self,
        coordinator: EZVIZSleepCompanionDataUpdateCoordinator,
        sensor_type: str,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        
        self._sensor_type = sensor_type
        self._entry = entry
        self._sensor_data = SENSOR_TYPE_MAP[sensor_type]
        
        # 设置实体ID
        self._attr_unique_id = f"{entry.entry_id}_{sensor_type}"
        self._attr_name = self._sensor_data["name"]
        self._attr_icon = self._sensor_data["icon"]
        self._attr_native_unit_of_measurement = self._sensor_data["unit"]
        self._attr_device_class = self._sensor_data["device_class"]
        self._attr_state_class = self._sensor_data["state_class"]
        
        # 设置设备信息
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            manufacturer="EZVIZ",
            model=self.coordinator.data.get(ATTR_DEVICE_MODEL, "Sleep Companion"),
            name=entry.data.get(CONF_DEVICE_NAME, DEFAULT_NAME),
            sw_version=self.coordinator.data.get(ATTR_SOFTWARE_VERSION),
        )

    @property
    def native_value(self) -> StateType:
        """Return the state of the sensor."""
        return self.coordinator.data.get(self._sensor_data["attr"])

    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        """Return the state attributes."""
        attrs = {
            ATTR_ATTRIBUTION: ATTRIBUTION,
        }
        
        # 添加其他相关属性
        if self._sensor_type == "sleep_score":
            attrs.update(
                {
                    ATTR_BED_TIME: self.coordinator.data.get(ATTR_BED_TIME),
                    ATTR_WAKE_UP_TIME: self.coordinator.data.get(ATTR_WAKE_UP_TIME),
                    ATTR_SLEEP_STATE: self.coordinator.data.get(ATTR_SLEEP_STATE),
                }
            )
        
        return attrs

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self.async_write_ha_state()
