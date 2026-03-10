from playwright.sync_api import Page, expect
from .base_page import BasePage
from utils.env_loader import get_env
from utils.data_reader import DataReader

ENV = get_env()
config = DataReader.load_json(f"configs/{ENV}.json")


class LoginPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)
        self.login_btn      = page.get_by_role("button", name="Login")
        self.email_input    = page.get_by_role("textbox", name="Email Address *")
        self.password_input = page.get_by_role("textbox", name="Password *")
        self.sign_in_button = page.get_by_role("button", name="Sign In")
        self.welcome_text   = page.get_by_text("Welcome to Multi Agent")
        self.new_chat_btn   = page.get_by_role("button", name="New Chat")

    def navigate(self):
        self.navigate_to(config["base_url"])
        self.login_btn.click()

    def login(self, email: str, password: str):
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.sign_in_button.click()

    def verify_page_loaded(self):
        expect(self.email_input).to_be_visible()
        expect(self.password_input).to_be_visible()
        expect(self.sign_in_button).to_be_visible()

    def verify_login_success(self):
        expect(self.welcome_text).to_be_visible()

    def verify_new_chat_btn_present(self):
        expect(self.new_chat_btn).to_be_visible()