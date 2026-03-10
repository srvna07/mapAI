import pytest
from pages.login_page import LoginPage


# goes through full login flow - does not reuse session
@pytest.mark.high
def test_valid_login_redirects(login_page, credentials):
    login_page.navigate()
    login_page.login(credentials["username"], credentials["password"])
    login_page.verify_login_success()


# reuses saved auth session - no login
@pytest.mark.smoke
def test_valid_login_shows_welcome(authenticated_page):
    page = LoginPage(authenticated_page)
    page.verify_login_success()


# reuses saved auth session - no login
@pytest.mark.smoke
def test_new_chat_btn_is_present(authenticated_page):
    page = LoginPage(authenticated_page)
    page.verify_new_chat_btn_present()