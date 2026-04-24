import pytest
from utils.api_client import APIClient
from utils.data_reader import DataReader
from utils.env_loader import get_env
import requests
import os
from utils.data_factory import DataFactory
import uuid

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

@pytest.fixture
def role_data():
    return DataReader.load_json("testdata/new_role_data.json")

@pytest.fixture
def update_payload(role_id, data):
    return {
        "roleName": data["edited_role"]["name"]
    }

@pytest.fixture(scope="function")
def new_organization_data():
    data = DataReader.load_json("testdata/new_organization.json")
    data["organization"]["name"] = DataFactory.generate_org_name()
    return data

@pytest.fixture(scope="function")
def invalid_organization_data():
    return DataReader.load_json("testdata/new_organization.json")

@pytest.fixture(scope="function")
def update_organization_data():
    data = DataReader.load_json("testdata/update_org.json")
    data["organization"]["name"] = DataFactory.generate_org_name()
    return data

@pytest.fixture(scope="function")
def user_test_data():
    return DataReader.load_json("testdata/new_user.json")

@pytest.fixture(scope="function")
def new_user_data():
    data = DataReader.load_json("testdata/new_user.json")

    data["user"]["email"] = DataFactory.random_email()
    data["user"]["firstName"] = DataFactory.random_name()
    data["user"]["lastName"] = DataFactory.random_name()

    return data






