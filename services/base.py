import logging
from abc import ABC
from typing import Any, Mapping

from httpx import Response

logger = logging.getLogger(__name__)


class BaseApiClient(ABC):
    @staticmethod
    def handler_response(
        response: Response, api_name: str
    ) -> Mapping[str, Any]:
        if response.status_code == 401:
            logger.error(f"{api_name}: неверный API-ключ (401)")
            raise Exception(f"{api_name}: неверный API-ключ (401)")
        if response.status_code == 429:
            logger.error(f"{api_name}: превышен лимит запросов (429)")
            raise Exception(f"{api_name}: превышен лимит запросов (429)")
        if response.status_code >= 400:
            logger.error(f"{api_name}: ошибка сервера ({response.status_code})")
            raise Exception(f"{api_name}: ошибка сервера ({response.status_code})")
        try:
            data = response.json()
            return data
        except Exception as e:
            logger.error(f"{api_name} error {response.status_code}: {e}")
            raise Exception(f"{api_name}: Error {response.status_code}")
