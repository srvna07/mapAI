import pytest
from playwright.sync_api import expect


@pytest.mark.smoke
def test_valid_login_shows_welcome(authenticated_page):
    expect(authenticated_page.get_by_text("Welcome to Multi Agent")).to_be_visible()