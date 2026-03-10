import pytest
from pathlib import Path
from datetime import datetime
from playwright.sync_api import Page, Browser

from utils.env_loader import get_env
from utils.data_reader import DataReader
from pages.login_page import LoginPage

ENV = get_env()
config = DataReader.load_json(f"configs/{ENV}.json")

AUTH_STATE_FILE = Path("test-results/.auth/state.json")


def apply_timeouts(pg):
    pg.set_default_timeout(config["default_timeout"])
    pg.set_default_navigation_timeout(config["navigation_timeout"])


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    return {**browser_type_launch_args, "args": ["--start-maximized"]}


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