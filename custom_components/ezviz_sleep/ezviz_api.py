"""萤石云API客户端."""
from __future__ import annotations

import logging
from typing import Any

import requests

from .const import API_BASE_URL

_LOGGER = logging.getLogger(__name__)


class EzvizSleepAPI:
    """萤石云睡眠伴侣API客户端."""

    def __init__(
        self,
        app_key: str,
        app_secret: str,
    ) -> None:
        """初始化API客户端."""
        self.app_key = app_key
        self.app_secret = app_secret
        self.access_token: str | None = None
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Content-Type": "application/x-www-form-urlencoded",
                "User-Agent": "HomeAssistant/EzvizSleep",
            }
        )

    def login(self) -> None:
        """登录萤石云获取AccessToken."""
        if not self.app_key or not self.app_secret:
            raise ValueError("AppKey/AppSecret 不能为空")

        url = f"{API_BASE_URL}/token/get"
        
        params = {
            "appKey": self.app_key,
            "appSecret": self.app_secret,
        }

        try:
            response = self.session.post(url, data=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            if data.get("code") == "200":
                self.access_token = data["data"]["accessToken"]
                _LOGGER.info("成功登录萤石云")
            else:
                raise Exception(f"登录失败: {data.get('msg', '未知错误')}")

        except requests.exceptions.RequestException as err:
            _LOGGER.error("登录请求失败: %s", err)
            raise

    def _make_request(
        self, endpoint: str, params: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """发送API请求."""
        if not self.access_token:
            self.login()

        url = f"{API_BASE_URL}{endpoint}"
        
        request_params = params or {}
        request_params["accessToken"] = self.access_token

        try:
            response = self.session.post(url, data=request_params, timeout=10)
            response.raise_for_status()
            data = response.json()

            if data.get("code") == "200":
                return data.get("data", {})
            elif data.get("code") == "10002":
                _LOGGER.warning("AccessToken过期，重新登录")
                self.login()
                request_params["accessToken"] = self.access_token
                response = self.session.post(url, data=request_params, timeout=10)
                response.raise_for_status()
                data = response.json()
                if data.get("code") == "200":
                    return data.get("data", {})
            
            raise Exception(f"API请求失败: {data.get('msg', '未知错误')}")

        except requests.exceptions.RequestException as err:
            _LOGGER.error("API请求失败: %s", err)
            raise

    def get_sleep_devices(self) -> list[dict[str, Any]]:
        """获取睡眠伴侣设备列表."""
        try:
            data = self._make_request("/device/list", {"pageStart": 0, "pageSize": 50})
            
            devices = []
            for device in data.get("list", []):
                if "sleep" in device.get("deviceType", "").lower():
                    devices.append(device)
            
            return devices
        except Exception as err:
            _LOGGER.error("获取设备列表失败: %s", err)
            return []

    def get_sleep_data(self, device_serial: str) -> dict[str, Any]:
        """获取睡眠数据."""
        try:
            data = self._make_request(
                "/sleep/realtime/data",
                {"deviceSerial": device_serial}
            )
            return data
        except Exception as err:
            _LOGGER.error("获取睡眠数据失败 (设备: %s): %s", device_serial, err)
            return {}

    def get_sleep_report(
        self, device_serial: str, date: str
    ) -> dict[str, Any]:
        """获取睡眠报告."""
        try:
            data = self._make_request(
                "/sleep/report",
                {"deviceSerial": device_serial, "date": date}
            )
            return data
        except Exception as err:
            _LOGGER.error("获取睡眠报告失败 (设备: %s, 日期: %s): %s", 
                         device_serial, date, err)
            return {}
