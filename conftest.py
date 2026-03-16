import os
import pytest
import json
from utils.env_loader import get_env
from utils.data_reader import DataReader
from utils.data_factory import DataFactory
from pages.login_page import LoginPage
from pages.users_page import UsersPage

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

# Users Page test data loading fixture
@pytest.fixture
def users_test_data():
    # Load your static JSON file
    # 1. Get the directory of THIS root conftest.py file
    root_path = os.path.dirname(os.path.abspath(__file__))
    
    # 2. Join it with the 'testdata' folder and the filename
    # This ensures it stays inside C:\Map AI\mapAI\
    path = os.path.join(root_path, "testdata", "users_page_test_data.json")
    with open(path) as f:
        data = json.load(f)

    # Setup Data for "Create"
    user = data["users"]
    user["first_name"] = DataFactory.generate_first_name()
    user["last_name"]  = DataFactory.generate_last_name()
    user["email"]      = DataFactory.random_email()
    user["phone"]      = DataFactory.generate_phone()
    user["password"]   = DataFactory.generate_password()

    # Setup Data for "Edit"
    edited = data["edited_users"]
    edited["first_name"] = DataFactory.generate_first_name(prefix="Edited")
    edited["last_name"]  = DataFactory.generate_last_name(prefix="Edited")
    user["email"]      = DataFactory.random_email(prefix="Edited")
    edited["phone"]      = DataFactory.generate_phone()

    return data