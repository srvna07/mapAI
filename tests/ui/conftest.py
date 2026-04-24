import json
import os
import pytest
from pathlib import Path
from datetime import datetime
from playwright.sync_api import Page, Browser
from utils.env_loader import get_env
from utils.api_client import APIClient
from utils.data_reader import DataReader
from utils.data_factory import DataFactory
from pages.login_page import LoginPage
from pages.role_page import RolePage
from pages.permission_page import PermissionPage
from pages.users_page import UsersPage
from pages.organizationPage import OrganizationsPage
from utils.data_factory import DataFactory
from pages.template_agent_page import TemplateAgentPage
from pages.mapAI_chat_page import MapAIChatPage


ENV = get_env()
config = DataReader.load_json(f"configs/{ENV}.json")

AUTH_STATE_FILE = Path("test-results/.auth/state.json")


def apply_timeouts(pg):
    pg.set_default_timeout(config["default_timeout"])
    pg.set_default_navigation_timeout(config["navigation_timeout"])


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    return {
        **browser_type_launch_args,
        "headless": False,
        "args": ["--start-maximized"]
    }


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    args = {
        **browser_context_args,
        "no_viewport": True,
        "record_video_size": config.get("record_video_size", {"width": 1280, "height": 720}),
    }
    if AUTH_STATE_FILE.exists():
        args["storage_state"] = str(AUTH_STATE_FILE)
    return args


@pytest.fixture(scope="session", autouse=True)
def setup_auth(browser: Browser, credentials):
    AUTH_STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    context = browser.new_context(no_viewport=True)
    pg = context.new_page()
    apply_timeouts(pg)
    login = LoginPage(pg)
    login.navigate()
    login.login(credentials["username"], credentials["password"])
    pg.wait_for_function(
        "() => { const auth = localStorage.getItem('persist:root'); if (!auth) return false; const parsed = JSON.parse(JSON.parse(auth).auth); return parsed.data !== null; }"
    )
    context.storage_state(path=str(AUTH_STATE_FILE))
    context.close()


@pytest.fixture
def authenticated_page(page: Page):
    apply_timeouts(page)
    page.goto(config["base_url"])
    return page


@pytest.fixture
def unauth_page(browser: Browser):
    context = browser.new_context(no_viewport=True)
    pg = context.new_page()
    apply_timeouts(pg)
    yield pg
    context.close()


@pytest.fixture
def login_page(unauth_page):
    return LoginPage(unauth_page)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        pg = item.funcargs.get("authenticated_page") or item.funcargs.get("unauth_page")
        if pg:
            screenshots_dir = Path(__file__).parent.parent.parent / "screenshots"
            screenshots_dir.mkdir(exist_ok=True)
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            pg.screenshot(path=str(screenshots_dir / f"{item.name}_{timestamp}.png"), full_page=True)


# Users page fixture
@pytest.fixture
def users_page(page):
    users_page_obj = UsersPage(page)
    return users_page_obj

@pytest.fixture(scope = "session")
def users_test_data():
    # Load your static JSON file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(current_dir, "..", "..", "testdata", "users_page_test_data.json")
    with open(path) as f:
        data = json.load(f)

    # Setup Data for Organization Creation
    organization = data["organization"]
    organization["name"] = DataFactory.generate_org_name()

    # Setup another organization for test
    another_organization = data["another_organization"]
    another_organization["name"] = DataFactory.generate_org_name(prefix = "test_another_org_")

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
    edited["email"]      = DataFactory.random_email(prefix="Edited")
    edited["phone"]      = DataFactory.generate_phone()

    return data


# Organization page fixture
@pytest.fixture
def organization_page(page):
    return OrganizationsPage(page)

@pytest.fixture(scope="session")
def new_organization_data():
    data = DataReader.load_yaml("testdata/new_organization.yaml")
    data["organization"]["name"]   = DataFactory.generate_org_name()
    return data

@pytest.fixture(scope="session")
def update_organization_data():
    return DataReader.load_json("testdata/update_org.json")

@pytest.fixture
def role_page(page):
    return RolePage(page)

@pytest.fixture(scope="session")
def new_role_data():
    data = DataReader.load_json("testdata/new_role_data.json")
    data["role"]["name"] = DataFactory.generate_role_name()
    return data

@pytest.fixture
def permission_page(page):
    return PermissionPage(page)
    
@pytest.fixture(scope="session")
def new_permission_data():
    data = DataReader.load_json("testdata/new_permission_data.json")
    data["permission"]["name"] = DataFactory.random_name(prefix="test_permission_")
    return data

@pytest.fixture
def api_client(authenticated_page) -> APIClient:
    client = APIClient(base_url=config["api_url"])
    token = authenticated_page.evaluate("localStorage.getItem('accessToken')")
    client.set_token(token)
    return client

@pytest.fixture(scope="session")
def new_template_agent_data():
    data = DataReader.load_json("testdata/template_agent_data.json")
    data["template_agent"]["name"] = DataFactory.random_name(prefix="test_template_agent_")
    return data

@pytest.fixture
def agent_page(page):
    return TemplateAgentPage(page)

@pytest.fixture
def new_chat_page(page):
    return MapAIChatPage(page)
