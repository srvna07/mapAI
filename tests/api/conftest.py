import pytest
from utils.api_client import APIClient
from utils.data_reader import DataReader
from utils.env_loader import get_env
import requests
import os
from utils.data_factory import DataFactory

ENV = get_env()
config = DataReader.load_json(f"configs/{ENV}.json")



def get_api_token():
    response = requests.post(
        f"{config['api_url']}/api/v1/auth/sign-in",
        json={
            "email": os.getenv("APP_USERNAME"),
            "password": os.getenv("APP_PASSWORD"),
            "roleId": os.getenv("Role_id"),
            "organizationId": os.getenv("organizationId"),
        }
    )
    assert response.status_code == 200, f"Login failed: {response.text}"

    return response.json()["accessToken"]


@pytest.fixture(scope="session")
def api_client() -> APIClient:
    client = APIClient(base_url=config["api_url"])

    token = get_api_token()   # API login 
    client.set_token(token)

    return client

@pytest.fixture(scope="session")
def new_organization_data():
    data = DataReader.load_yaml("testdata/new_organization.yaml")
    data["organization"]["name"] = DataFactory.generate_org_name()
    return data
