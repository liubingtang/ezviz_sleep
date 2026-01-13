"""Binary sensor platform for EZVIZ Sleep Companion."""
from __future__ import annotations

import logging
from typing import Any, Dict, Optional

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    ATTR_DEVICE_MODEL,
    ATTR_LAST_UPDATE,
    ATTR_SLEEP_STATE,
    ATTR_SOFTWARE_VERSION,
    ATTRIBUTION,
    BINARY_SENSOR_TYPES,
    CONF_DEVICE_NAME,
    DEFAULT_NAME,
    DOMAIN,
)
from .coordinator import EZVIZSleepCompanionDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

# 二进制传感器类型与属性的映射
BINARY_SENSOR_MAP = {
    "in_bed": {
        "attr": "in_bed",
        "device_class": BinarySensorDeviceClass.OCCUPANCY,
        "icon": "mdi:bed-king",
        "name": "In Bed",
    },
    "asleep": {
        "attr": "asleep",
        "device_class": None,
        "icon": "mdi:sleep",
        "name": "Asleep",
    },
}


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up EZVIZ Sleep Companion binary sensors based on a config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    
    # 为每种二进制传感器类型创建一个实体
    entities = [
        EZVIZSleepCompanionBinarySensor(coordinator, sensor_type, entry)
        for sensor_type in BINARY_SENSOR_MAP
    ]
    
    async_add_entities(entities, True)


class EZVIZSleepCompanionBinarySensor(
    CoordinatorEntity[EZVIZSleepCompanionDataUpdateCoordinator], BinarySensorEntity
):
    """Representation of an EZVIZ Sleep Companion binary sensor."""

    _attr_has_entity_name = True
    _attr_should_poll = False

    def __init__(
        self,
        coordinator: EZVIZSleepCompanionDataUpdateCoordinator,
        sensor_type: str,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the binary sensor."""
        super().__init__(coordinator)
        
        self._sensor_type = sensor_type
        self._entry = entry
        self._sensor_data = BINARY_SENSOR_MAP[sensor_type]
        
        # 设置实体ID
        self._attr_unique_id = f"{entry.entry_id}_{sensor_type}"
        self._attr_name = self._sensor_data["name"]
        self._attr_icon = self._sensor_data["icon"]
        self._attr_device_class = self._sensor_data["device_class"]
        
        # 设置设备信息
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            manufacturer="EZVIZ",
            model=self.coordinator.data.get(ATTR_DEVICE_MODEL, "Sleep Companion"),
            name=entry.data.get(CONF_DEVICE_NAME, DEFAULT_NAME),
            sw_version=self.coordinator.data.get(ATTR_SOFTWARE_VERSION),
        )

    @property
    def is_on(self) -> bool | None:
        """Return the state of the binary sensor."""
        return self.coordinator.data.get(self._sensor_data["attr"])

    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        """Return the state attributes."""
        attrs = {
            ATTR_ATTRIBUTION: ATTRIBUTION,
        }
        
        # 添加最后更新时间
        if last_update := self.coordinator.data.get(ATTR_LAST_UPDATE):
            attrs[ATTR_LAST_UPDATE] = last_update
        
        return attrs

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self.async_write_ha_state()
