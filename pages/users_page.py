import pytest
from pages.base_page import BasePage
from playwright.sync_api import expect

class UsersPage(BasePage):
    # Locators
    def __init__(self, page):
        super().__init__(page)
        
        #navigation
        self.menu = page.get_by_label("Directory")
        self.users_page_button = page.get_by_role("menuitem", name="Users")

        #search and add user button
        self.search_bar = page.get_by_role("textbox", name="Search by Name")
        self.add_user_button = page.get_by_role("button", name="Add User")

        #table locators
        self.table_row = page.get_by_role("row")

        #add user form
        self.first_name_textbox = page.get_by_role("textbox", name="First Name")
        self.last_name_testbox = page.get_by_role("textbox", name="Last Name")
        self.email_textbox = page.get_by_role("textbox", name="Email")
        self.phone_number_textbox = page.get_by_role("textbox", name="Phone Number")
        self.role_combobox = page.get_by_role("combobox", name="Role")
        self.organization_combobox = page.get_by_role("combobox", name="Organization")
        self.agent_combobox = page.get_by_role("combobox", name="Agent")
        self.password_textbox = page.get_by_role("textbox", name="Password")
        self.save_button = page.get_by_role("button", name="Save")
        self.cancel_button = page.get_by_role("button", name="Cancel")

        #edit user
        self.edit_user_button = page.get_by_role("button").nth(1)
        self.edit_user_confirmation_button = page.get_by_role("button", name="Yes, Proceed")

        #delete suer 
        self.delete_user_button = page.get_by_role("button").nth(2)
        self.delete_user_confirmation_button = page.get_by_role("button", name="Delete")

        #pagination
        self.go_to_next_page = page.get_by_role("button", name="Go to next page")
        self.go_to_previous_page = page.get_by_role("button", name="Go to previous page")
        self.rows_per_page_menu = page.get_by_role("combobox", name="Rows per page:")
        self.rows_per_page_option = self.rows_per_page_menu.get_by_role("option")
        self.pagination_label = page.locator(".MuiTablePagination-displayedRows")

        #close button
        self.close_button = page.get_by_role("button", name="close")

        # Search and found no data
        self.verify_search_data_not_available = page.get_by_text("No data available")
        

    # Actions
    def navigate_to_users_page(self):
        self.menu.click()
        self.users_page_button.click()

    def search_user(self, user_name):
        self.search_bar.click()
        self.search_bar.fill(user_name)

    def click_add_user_button(self):
        self.add_user_button.click()

    def click_edit_button(self):
        self.edit_user_button.click()

    def click_edit_user_confirmation_button(self):
        self.edit_user_confirmation_button.click()

    def click_delete_user_button(self):
        self.delete_user_button.click()

    def click_delete_confirmation_button(self):
        self.delete_user_confirmation_button.click()

    def fill_first_name(self, first_name):
        self.first_name_textbox.fill(first_name)

    def fill_last_name(self, last_name):
        self.last_name_testbox.fill(last_name)

    def fill_email_textbox(self, email):
        self.email_textbox.fill(email)

    def fill_phone_number(self, phone):
        self.phone_number_textbox.fill(phone)

    def select_role(self, role_name):
        self.role_combobox.click()
        self.page.get_by_role("option", name=role_name, exact=True).click()

    def select_organization(self, organization_name):
        self.organization_combobox.click()
        self.page.get_by_role("option", name=organization_name, exact=True).click()

    def select_agent(self, combined_agent):
        self.agent_combobox.click()
        self.page.get_by_role("option", name=combined_agent, exact=True).click()
        # self.page.wait_for_timeout(700)
        self.page.keyboard.press("Escape")

    def fill_password_textbox(self, password):
        self.password_textbox.fill(password)

    def click_save_button(self):
        self.save_button.click()

    def click_cancel_button(self):
        self.cancel_button.click()

    def click_delete_button(self):
        self.delete_user_button.click()

    def click_go_to_next_page(self):
        old_text = self.pagination_label.inner_text()
        expect(self.go_to_next_page).to_be_enabled()
        self.page.wait_for_timeout(1000)
        self.go_to_next_page.click()
        expect(self.pagination_label).not_to_have_text(old_text, timeout=10000)

    def click_go_to_previous_page(self):
        old_text = self.pagination_label.inner_text()
        expect(self.go_to_previous_page).to_be_enabled()
        self.page.wait_for_timeout(1000)
        self.go_to_previous_page.click()
        expect(self.pagination_label).not_to_have_text(old_text, timeout=5000)

    def select_rows_per_page(self, row_count):
        self.rows_per_page_menu.click()
        self.page.get_by_role("option", name=str(row_count)).click()

    def get_toast_message(self, message: str, timeout=15000):
        toast = self.page.get_by_text(message)
        toast.wait_for(state="visible", timeout=timeout)
        return toast

    def click_close_button(self):
        self.close_button.click()

    def verify_table_is_empty(self):
        expect(self.verify_search_data_not_available).to_be_visible()

    def verify_search_item_in_table(self, search_item_name: str):
        expect(self.page.get_by_text(search_item_name).first).to_be_visible()

    def get_table_row_count(self):
        return self.page.locator("tbody tr").count()
    
    def verify_pagination_limit(self, expected_limit):
        self.page.locator("tbody tr").first.wait_for(state="visible", timeout=5000)
        self.page.wait_for_timeout(500) 
        actual_rows = self.get_table_row_count()
        assert actual_rows <= int(expected_limit), f"Table showing {actual_rows} rows, exceeding limit of {expected_limit}"

    def verify_page_label_contains(self, text):
        expect(self.pagination_label).to_contain_text(text)