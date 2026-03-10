import pytest
from utils.api_client import APIClient
from utils.data_reader import DataReader
from utils.env_loader import get_env

ENV = get_env()
config = DataReader.load_json(f"configs/{ENV}.json")


@pytest.fixture(scope="session")
def api_client() -> APIClient:
    return APIClient(base_url=config["api_url"])
