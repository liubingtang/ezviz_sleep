"""API client for EZVIZ Sleep Companion."""
from __future__ import annotations

import aiohttp
import async_timeout
import hashlib
import hmac
import json
import logging
import time
from typing import Any, Dict, Optional

from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import BASE_URL, API_TIMEOUT

_LOGGER = logging.getLogger(__name__)

class EZVIZAPIError(Exception):
    """EZVIZ API error."""
    pass

class EZVIZSleepCompanionAPI:
    """EZVIZ Sleep Companion API client."""

    def __init__(
        self,
        hass: HomeAssistant,
        app_key: str,
        app_secret: str,
        device_serial: str,
    ) -> None:
        """Initialize the API client."""
        self._hass = hass
        self._app_key = app_key
        self._app_secret = app_secret
        self._device_serial = device_serial
        self._access_token: Optional[str] = None
        self._token_expire_time: float = 0

    async def async_authenticate(self) -> str:
        """Authenticate with EZVIZ API and get access token."""
        if self._access_token and time.time() < self._token_expire_time - 60:  # 提前1分钟刷新
            return self._access_token

        url = f"{BASE_URL}/api/lapp/token/get"
        
        data = {
            "appKey": self._app_key,
            "appSecret": self._app_secret
        }
        
        response = await self._async_request("post", url, data=data, auth_required=False)
        
        self._access_token = response["data"]["accessToken"]
        # 设置token过期时间，默认6小时有效期，这里设置为5小时50分钟
        self._token_expire_time = time.time() + 21000  # 5小时50分钟，单位秒
        
        return self._access_token

    async def async_get_device_info(self) -> Dict[str, Any]:
        """Get device information."""
        url = f"{BASE_URL}/api/lapp/device/info"
        data = {
            "deviceSerial": self._device_serial,
            "deviceType": "INFRARED_SLEEP_COMPANION"  # 假设设备类型
        }
        
        response = await self._async_request("post", url, data=data)
        return response["data"]

    async def async_get_sleep_data(self) -> Dict[str, Any]:
        """Get sleep data from the device."""
        # 这里需要根据实际API调整
        url = f"{BASE_URL}/api/lapp/device/sleep/data"
        
        # 获取当天日期
        today = time.strftime("%Y-%m-%d", time.localtime())
        
        data = {
            "deviceSerial": self._device_serial,
            "date": today
        }
        
        response = await self._async_request("post", url, data=data)
        return response["data"]

    async def _async_request(
        self,
        method: str,
        url: str,
        data: Optional[Dict[str, Any]] = None,
        auth_required: bool = True,
    ) -> Dict[str, Any]:
        """Make an API request."""
        if data is None:
            data = {}
            
        headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        }
        
        # 如果需要认证，添加access token
        if auth_required:
            access_token = await self.async_authenticate()
            headers["accessToken"] = access_token
        
        # 添加公共参数
        data["accessToken"] = headers.get("accessToken", "")
        
        # 生成签名
        data["sign"] = self._generate_sign(data)
        
        _LOGGER.debug("Sending request to %s: %s", url, data)
        
        session = async_get_clientsession(self._hass)
        
        try:
            async with async_timeout.timeout(API_TIMEOUT):
                if method.lower() == "get":
                    response = await session.get(url, params=data, headers=headers)
                else:
                    response = await session.post(url, data=data, headers=headers)
                
                if response.status != 200:
                    raise EZVIZAPIError(f"HTTP {response.status}")
                
                result = await response.json()
                _LOGGER.debug("Response from API: %s", result)
                
                # 检查API返回的错误码
                if "code" in result and result["code"] != "200":
                    error_msg = result.get("msg", "Unknown error")
                    raise EZVIZAPIError(f"API error: {error_msg} (code: {result['code']})")
                
                return result
                
        except asyncio.TimeoutError as err:
            raise EZVIZAPIError("Timeout while connecting to EZVIZ API") from err
            
        except (aiohttp.ClientError, json.JSONDecodeError) as err:
            raise EZVIZAPIError("Error communicating with EZVIZ API") from err
    
    def _generate_sign(self, params: Dict[str, Any]) -> str:
        """Generate API request signature."""
        # 1. 对参数按照key进行排序
        sorted_params = sorted(params.items(), key=lambda x: x[0])
        
        # 2. 拼接参数字符串
        param_str = ""
        for k, v in sorted_params:
            if k != "sign" and v is not None:  # 排除sign参数和空值参数
                param_str += f"{k}{v}"
        
        # 3. 拼接appSecret
        sign_str = f"{param_str}{self._app_secret}"
        
        # 4. 计算MD5
        sign = hashlib.md5(sign_str.encode('utf-8')).hexdigest().upper()
        
        return sign
