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
        self.last_name_textbox = page.get_by_role("textbox", name="Last Name")
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

        #delete user 
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
        self.last_name_textbox.fill(last_name)

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

    def select_agent(self, agent_name):
        self.agent_combobox.click()
        self.page.get_by_role("option", name=agent_name, exact=True).click()
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
        self.go_to_next_page.click()
        expect(self.pagination_label).not_to_have_text(old_text, timeout=5000)

    def click_go_to_previous_page(self):
        old_text = self.pagination_label.inner_text()
        expect(self.go_to_previous_page).to_be_enabled()
        self.go_to_previous_page.click()
        expect(self.pagination_label).not_to_have_text(old_text, timeout=5000)

    def select_rows_per_page(self, row_count):
        self.rows_per_page_menu.click()
        self.page.get_by_role("option", name=str(row_count)).click()

    def get_toast_message(self, message: str):
        return self.page.get_by_text(message)

    def click_close_button(self):
        self.close_button.click()

    def verify_table_is_empty(self):
        expect(self.verify_search_data_not_available).to_be_visible()

    def verify_search_item_in_table(self, search_item_name: str):
        row = self.page.locator("tbody tr", has_text=search_item_name)
        expect(row.first).to_be_visible()

    def get_table_row_count(self):
        return self.page.locator("tbody tr").count()
    
    def verify_pagination_limit(self, expected_limit):
        self.page.locator("tbody tr").first.wait_for(state="visible", timeout=5000)
        self.page.wait_for_timeout(500) 
        actual_rows = self.get_table_row_count()
        assert actual_rows <= int(expected_limit), f"Table showing {actual_rows} rows, exceeding limit of {expected_limit}"

    def verify_page_label_contains(self, text):
        expect(self.pagination_label).to_contain_text(text)

    def get_dropdown_option(self, name):
        return self.page.get_by_role("option", name=name, exact=True)
    
    def select_dropdown_value(self, combobox, value):
        combobox.click()
        self.get_dropdown_option(value).click()

    def verify_agents_visible(self, agents):
        self.wait_for_agents_loaded(agents)
        for agent in agents:
            expect(self.get_dropdown_option(agent)).to_be_visible()

    def close_agent_dropdown(self):
        self.page.keyboard.press("Escape")
          


    def open_agent_dropdown(self):
        expect(self.agent_combobox).to_be_visible()
        expect(self.agent_combobox).to_be_enabled()
        self.agent_combobox.click()

    def close_dropdown(self):
        self.page.keyboard.press("Escape")

    def get_agent_options(self):
        return self.page.get_by_role("option")

    def get_agent_count(self):
        return self.get_agent_options().count()

    def get_all_agent_names(self):
        return self.get_agent_options().all_text_contents()

    def verify_agents_visible(self, agents):
        for agent in agents:
            expect(self.page.get_by_role("option", name=agent)).to_be_visible()

    def verify_agents_not_visible(self, agents):
        options = self.get_all_agent_names()

        for agent in agents:
            assert agent not in options, f"Agent '{agent}' still visible in dropdown"

    def verify_no_agents_message(self):
        expect(self.page.get_by_text("No agents available")).to_be_visible()
    
    def get_agents_for_organization(self, org_name):
        self.select_organization(org_name)
        self.open_agent_dropdown()
        agents = self.get_all_agent_names()
        self.close_dropdown()
        return agents
    
    def open_organization_dropdown(self):
        self.organization_combobox.click()

    def verify_organization_not_present(self, org_name):
        expect(self.page.get_by_role("option", name=org_name)).not_to_be_visible()
    def unselect_agents(self, agents):
        self.open_agent_dropdown()

        for agent in agents:
            option = self.page.get_by_role("option", name=agent)

        # Wait for option to be visible
            expect(option).to_be_visible()

        # Check selection state properly
            if option.get_attribute("aria-selected") == "true":
             option.click()

        self.agent_dropdown.press("Escape")