import os
import pytest
from dotenv import load_dotenv
from pages.login_page import LoginPage
from pages.organizationPage import OrganizationsPage
from pages.users_page import UsersPage

from utils.env_loader import get_env
from utils.data_reader import DataReader

load_dotenv()

@pytest.fixture(scope="session")
def env_config():
    env = get_env()
    return DataReader.load_json(f"configs/{env}.json")

@pytest.fixture(scope="session")
def credentials():
    username = os.getenv("APP_USERNAME")
    password = os.getenv("APP_PASSWORD")
    if not username or not password:
        pytest.exit("❌ APP_USERNAME / APP_PASSWORD not set in .env", returncode=1)
    return {"username": username, "password": password}

@pytest.fixture(scope="session")
def authenticated_page(browser):
    context = browser.new_context()
    page = context.new_page()

    login = LoginPage(page)
    login.navigate()
    login.login(os.getenv("APP_USERNAME"), os.getenv("APP_PASSWORD"))
    login.verify_login_success()

    yield page

    context.close()

@pytest.fixture
def organization_page(authenticated_page):
    return OrganizationsPage(authenticated_page)

@pytest.fixture
def users_page(authenticated_page):
    return UsersPage(authenticated_page)


@pytest.fixture(scope="session")
def integration_data():
    # Corrected path based on your input
    return DataReader.load_json("testdata/user_org_data.json")