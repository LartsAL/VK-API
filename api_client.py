import requests
import time
from config import VK_ACCESS_TOKEN, VK_API_VERSION, VK_API_BASE_URL, REQUEST_DELAY
from typing import Dict, Any, Optional


class VKAPIException(Exception):
    def __init__(self, error_data: Dict[str, Any]):
        self.code = error_data.get('error_code', 0)
        self.message = error_data.get('error_msg', 'Unknown error')
        self.request_params = error_data.get('request_params', [])
        super().__init__(f"VK API Error {self.code}: {self.message}")


def call_vk_api(method: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    if not VK_ACCESS_TOKEN:
        raise ValueError("VK access token is not configured")

    request_params = params or {}
    request_params.update({
        'v': VK_API_VERSION,
        'access_token': VK_ACCESS_TOKEN
    })

    try:
        response = requests.post(
            f"{VK_API_BASE_URL}{method}",
            data=request_params,
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"Network error: {str(e)}") from e

    if 'error' in data:
        raise VKAPIException(data['error'])

    time.sleep(REQUEST_DELAY)

    return data.get('response', {})