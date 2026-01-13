"""萤石云无感睡眠伴侣常量."""

DOMAIN = "ezviz_sleep"

API_BASE_URL = "https://open.ys7.com/api/lapp"

CONF_APP_KEY = "app_key"
CONF_APP_SECRET = "app_secret"

CONF_ENABLE_HEART_RATE = "enable_heart_rate"
CONF_ENABLE_BREATH_RATE = "enable_breath_rate"
CONF_ENABLE_SLEEP_STATUS = "enable_sleep_status"
CONF_ENABLE_BODY_MOVEMENT = "enable_body_movement"
CONF_ENABLE_SLEEP_SCORE = "enable_sleep_score"
CONF_ENABLE_SLEEP_DURATION = "enable_sleep_duration"

ATTR_HEART_RATE = "heart_rate"
ATTR_BREATH_RATE = "breath_rate"
ATTR_SLEEP_STATUS = "sleep_status"
ATTR_BODY_MOVEMENT = "body_movement"
ATTR_SLEEP_SCORE = "sleep_score"
ATTR_DEEP_SLEEP = "deep_sleep"
ATTR_LIGHT_SLEEP = "light_sleep"
ATTR_AWAKE_TIME = "awake_time"
ATTR_DEVICE_SERIAL = "device_serial"
ATTR_DEVICE_NAME = "device_name"

SLEEP_STATUS_MAP = {
    0: "离床",
    1: "清醒",
    2: "浅睡",
    3: "深睡",
    4: "REM睡眠",
}
