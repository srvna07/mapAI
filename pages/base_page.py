import re
from playwright.sync_api import Page, Locator, expect


class BasePage:

    def __init__(self, page: Page):
        self.page = page

    def navigate_to(self, url: str):
        self.page.goto(url)
        self.page.wait_for_load_state("domcontentloaded")

    def navigate_to_and_wait_network(self, url: str):
        self.page.goto(url)
        self.page.wait_for_load_state("networkidle")

    def assert_url_contains(self, fragment: str):
        expect(self.page).to_have_url(re.compile(re.escape(fragment)))

    def assert_visible(self, locator: Locator):
        expect(locator).to_be_visible()

    def select_dropdown_by_label(self, dropdown: Locator, label: str):
        dropdown.click()
        self.page.wait_for_load_state("domcontentloaded")
        option = self.page.get_by_role("option", name=label, exact=True)
        expect(option).to_be_visible()
        option.click()
