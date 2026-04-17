import pytest
from pages.base_page import BasePage
from playwright.sync_api import expect

class TemplateAgentPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.menu = page.get_by_label("Directory")
        self.agents_page_button = page.get_by_role("menuitem", name="Template Agents")
        self.add_template_agent_button = page.get_by_role("button", name="Add Template Agent")
        self.name_textbox = page.get_by_role("textbox", name="Name *")
        self.combobox = page.get_by_role("combobox")
        self.option = page.get_by_role("option", name="gpt-4o-")
        self.instructions_textbox = page.get_by_role("textbox", name="Instructions *")
        self.save_button = page.get_by_role("button", name="Save")
        self.confirm_delete_button = page.get_by_role("button", name="Delete")
        self.success_message = page.get_by_text("Template Agent Created")
        self.update_message = page.get_by_text("Template Agent Updated")
        self.search_textbox = page.get_by_role("textbox", name="Search by Name")
        self.edit_button = page.get_by_role("button").nth(1)
        self.delete_button = page.get_by_role("button").nth(2)
        self.verify_search_data_not_available = page.get_by_text("No data found")
        self.delete_message = page.get_by_text("Template Agent Deleted")

    def navigate_to_agents_page(self):
        self.menu.click()
        self.agents_page_button.click()

    def add_template_agent(self, name, instructions):
        self.add_template_agent_button.click()
        self.name_textbox.fill(name)
        self.combobox.click()
        self.option.click()
        self.instructions_textbox.fill(instructions)
        self.save_button.click()
        self.success_message.wait_for(state="visible")

    def edit_template_agent(self, old_name, new_name, new_instructions):
        self.search_textbox.fill(old_name)
        row = self.page.locator("tr", has_text=old_name).first
        row.wait_for(state="visible")
        row.locator("button").nth(0).click()  # Click edit button in the row
    
        self.name_textbox.fill(new_name)
        self.instructions_textbox.fill(new_instructions)
        self.save_button.click()
        self.update_message.wait_for(state="visible")

    def delete_template_agent(self, name):
        self.search_textbox.fill(name)
        row = self.page.locator("tr", has_text=name).first
        row.wait_for(state="visible")
        # Click delete icon in row
        row.locator("button").nth(1).click()
        self.confirm_delete_button.click()
        self.delete_message.wait_for(state="visible")

    # Verification methods
    def verify_template_agent_in_table(self, name):
        self.navigate_to_agents_page()  # Ensure we are on the agents page
        self.search_textbox.fill(name)
        expect(self.page.get_by_role("cell", name=name)).to_be_visible()       

    def verify_template_agent_not_in_table(self, name):
        self.navigate_to_agents_page()  # Ensure we are on the agents page
        self.search_textbox.fill(name)
        expect(self.verify_search_data_not_available).to_be_visible()
    