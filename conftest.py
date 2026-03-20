import os
import pytest
from utils.env_loader import get_env
from utils.data_reader import DataReader

ENV = get_env()
config = DataReader.load_json(f"configs/{ENV}.json")


@pytest.fixture(scope="session")
def config_fixture():
    return config


@pytest.fixture(scope="session")
def credentials():
    username = os.getenv("APP_USERNAME")
    password = os.getenv("APP_PASSWORD")
    if not username or not password:
        pytest.exit("APP_USERNAME / APP_PASSWORD not set in .env", returncode=1)
    return {"username": username, "password": password}