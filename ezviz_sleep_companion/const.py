"""Constants for the EZVIZ Sleep Companion integration."""
from __future__ import annotations

from typing import Final

# Base component constants
DOMAIN: Final = "ezviz_sleep_companion"
NAME: Final = "EZVIZ Sleep Companion"
VERSION: Final = "0.1.0"
ATTRIBUTION: Final = "Data provided by EZVIZ Cloud"
ISSUE_URL: Final = "https://github.com/yourusername/ezviz-sleep-companion-ha/issues"

# Icons
ICON: Final = "mdi:bed-king"

# Platforms
PLATFORMS: Final = ["sensor", "binary_sensor"]

# Configuration
CONF_APP_KEY: Final = "app_key"
CONF_APP_SECRET: Final = "app_secret"
CONF_DEVICE_SERIAL: Final = "device_serial"
CONF_DEVICE_NAME: Final = "device_name"
CONF_UPDATE_INTERVAL: Final = "update_interval"

# Defaults
DEFAULT_NAME: Final = "EZVIZ Sleep Companion"
DEFAULT_UPDATE_INTERVAL: Final = 300  # 5 minutes

# API
BASE_URL: Final = "https://open.ys7.com"
API_TIMEOUT: Final = 10

# Attributes
ATTR_DEVICE_MODEL: Final = "device_model"
ATTR_SOFTWARE_VERSION: Final = "software_version"
ATTR_LAST_UPDATE: Final = "last_update"
ATTR_SLEEP_SCORE: Final = "sleep_score"
ATTR_HEART_RATE: Final = "heart_rate"
ATTR_BREATHING_RATE: Final = "breathing_rate"
ATTR_SLEEP_STATE: Final = "sleep_state"
ATTR_BED_TIME: Final = "bed_time"
ATTR_WAKE_UP_TIME: Final = "wake_up_time"
ATTR_SLEEP_DURATION: Final = "sleep_duration"
ATTR_DEEP_SLEEP_DURATION: Final = "deep_sleep_duration"
ATTR_LIGHT_SLEEP_DURATION: Final = "light_sleep_duration"
ATTR_AWAKE_DURATION: Final = "awake_duration"
ATTR_SLEEP_EFFICIENCY: Final = "sleep_efficiency"

# Device classes
SENSOR_TYPES: dict[str, dict[str, str]] = {
    "sleep_score": {
        "name": "Sleep Score",
        "icon": "mdi:sleep",
        "unit_of_measurement": "%",
        "device_class": None,
        "state_class": "measurement",
    },
    "heart_rate": {
        "name": "Heart Rate",
        "icon": "mdi:heart-pulse",
        "unit_of_measurement": "bpm",
        "device_class": "heart_rate",
        "state_class": "measurement",
    },
    "breathing_rate": {
        "name": "Breathing Rate",
        "icon": "mdi:weather-windy",
        "unit_of_measurement": "rpm",
        "device_class": None,
        "state_class": "measurement",
    },
    "sleep_duration": {
        "name": "Sleep Duration",
        "icon": "mdi:clock-time-eight-outline",
        "unit_of_measurement": "min",
        "device_class": "duration",
        "state_class": "measurement",
    },
    "deep_sleep_duration": {
        "name": "Deep Sleep Duration",
        "icon": "mdi:sleep",
        "unit_of_measurement": "min",
        "device_class": "duration",
        "state_class": "measurement",
    },
    "light_sleep_duration": {
        "name": "Light Sleep Duration",
        "icon": "mdi:sleep-off",
        "unit_of_measurement": "min",
        "device_class": "duration",
        "state_class": "measurement",
    },
    "awake_duration": {
        "name": "Awake Duration",
        "icon": "mdi:bed-clock",
        "unit_of_measurement": "min",
        "device_class": "duration",
        "state_class": "measurement",
    },
    "sleep_efficiency": {
        "name": "Sleep Efficiency",
        "icon": "mdi:chart-arc",
        "unit_of_measurement": "%",
        "device_class": None,
        "state_class": "measurement",
    },
}

BINARY_SENSOR_TYPES: dict[str, dict[str, str]] = {
    "in_bed": {
        "name": "In Bed",
        "icon": "mdi:bed-king",
        "device_class": "occupancy",
    },
    "asleep": {
        "name": "Asleep",
        "icon": "mdi:sleep",
        "device_class": None,
    },
}
