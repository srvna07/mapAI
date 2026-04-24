import pytest
from pages.base_page import BasePage
from playwright.sync_api import expect
from time import sleep

class RolePage(BasePage):
    def __init__(self, page):
        super().__init__(page)

        # Navigation
        self.menu                       = page.get_by_label("Directory")
        self.roles_page_button          = page.get_by_role("menuitem", name="Roles")
        self.search_bar                 = page.get_by_role("textbox", name="Search by Name")
        self.success_message            = page.get_by_text("Role created successfully")
        self.update_message             = page.get_by_text("Role Updated Successfully")
        self.delete_message             = page.get_by_text("Role Deleted Successfully")
        self.delete_role_confirmation_button = page.get_by_role("button", name="Delete")

        # Add Role
        self.add_role_button            = page.get_by_role("button", name="Add Role")
        
        self.role_name_textbox          = page.get_by_role("textbox", name="Role Name")
        self.save_button                = page.get_by_role("button", name="Save")
        self.cancel_button              = page.get_by_role("button", name="Cancel")
        self.edit_role_button           = page.get_by_role("button").nth(1)
        self.delete_role_button         = page.get_by_role("button").nth(2)

    def navigate_to_roles_page(self):
        self.menu.click()
        self.roles_page_button.click()

    def add_role(self, role_name):
        self.add_role_button.click()
        self.role_name_textbox.fill(role_name)
        self.save_button.click()
        self.success_message.wait_for(state="visible")

    def edit_role(self, old_role_name, new_role_name):
        self.search_bar.fill(old_role_name)
        row = self.page.locator("tr", has_text=old_role_name).first
        row.wait_for(state="visible")
        row.locator("button").nth(0).click()  # Click edit button in the row

        self.role_name_textbox.fill(new_role_name)
        self.save_button.click()
        self.update_message.wait_for(state="visible")

    def delete_role(self, role_name):
        self.search_bar.fill(role_name)
        row = self.page.locator("tr", has_text=role_name).first
        row.wait_for(state="visible")
        row.locator("button").nth(1).click()  # Click delete button in the row
        self.delete_role_confirmation_button.click()
        self.delete_message.wait_for(state="visible")

    # Verification methods
    def verify_role_in_table(self, role_name):
        self.navigate_to_roles_page()  # Ensure we are on the roles page
        self.search_bar.fill(role_name)
        expect(self.page.get_by_role("cell", name=role_name)).to_be_visible()

    def verify_role_not_in_table(self, role_name):
        self.navigate_to_roles_page()  # Ensure we are on the roles page
        self.search_bar.fill(role_name)
        expect(self.page.get_by_role("cell", name=role_name)).not_to_be_visible()