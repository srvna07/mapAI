import pytest
from pages.login_page import LoginPage

@pytest.mark.smoke
def test_valid_login_shows_welcome(authenticated_page):
    page = LoginPage(authenticated_page)
    page.verify_login_success()

@pytest.mark.smoke
def test_new_chat_btn_is_present(authenticated_page):
    page = LoginPage(authenticated_page)
    page.verify_new_chat_btn_present()