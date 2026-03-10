import requests
from utils.logger import get_logger

logger = get_logger(__name__)


class APIClient:

    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
        self.session  = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})

    def set_token(self, token: str):
        self.session.headers.update({"Authorization": f"Bearer {token}"})

    def set_headers(self, headers: dict):
        self.session.headers.update(headers)

    def get(self, endpoint: str, params: dict = None, **kwargs) -> requests.Response:
        response = self.session.get(self._url(endpoint), params=params, **kwargs)
        logger.info(f"GET {response.url} [{response.status_code}]")
        return response

    def post(self, endpoint: str, payload: dict = None, **kwargs) -> requests.Response:
        response = self.session.post(self._url(endpoint), json=payload, **kwargs)
        logger.info(f"POST {response.url} [{response.status_code}]")
        return response

    def put(self, endpoint: str, payload: dict = None, **kwargs) -> requests.Response:
        response = self.session.put(self._url(endpoint), json=payload, **kwargs)
        logger.info(f"PUT {response.url} [{response.status_code}]")
        return response

    def patch(self, endpoint: str, payload: dict = None, **kwargs) -> requests.Response:
        response = self.session.patch(self._url(endpoint), json=payload, **kwargs)
        logger.info(f"PATCH {response.url} [{response.status_code}]")
        return response

    def delete(self, endpoint: str, **kwargs) -> requests.Response:
        response = self.session.delete(self._url(endpoint), **kwargs)
        logger.info(f"DELETE {response.url} [{response.status_code}]")
        return response

    def _url(self, endpoint: str) -> str:
        return f"{self.base_url}/{endpoint.lstrip('/')}"
