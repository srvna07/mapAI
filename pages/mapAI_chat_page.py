import pytest
from pages.base_page import BasePage
from playwright.sync_api import expect

class MapAIChatPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.new_chat_btn = page.get_by_role("button", name="New Chat")
        self.agents_link = page.get_by_role("link", name="Agents")
        self.my_agents_heading = page.get_by_role("heading", name="My Agents")
        self.load_more_btn = page.get_by_role("button", name="Load More")
        self.message_input = page.get_by_role("textbox", name="Type your message...")
        self.send_button = page.get_by_role("button", name="Send")
        self.attach_file_button = page.get_by_role("button", name="attach file")
        self.record_audio_button = page.get_by_role("button", name="record audio")
        
    def verify_page_loaded(self):
        expect(self.new_chat_btn).to_be_visible()
        expect(self.agents_link).to_be_visible()
        expect(self.my_agents_heading).to_be_visible()
        expect(self.message_input).to_be_visible()
        expect(self.send_button).to_be_visible()
        expect(self.attach_file_button).to_be_visible()
        expect(self.record_audio_button).to_be_visible()

    def verify_agent_in_chat(self, combined_agent_name):
        self.agents_link.click()
        self.my_agents_heading.click()
        expect(self.page.get_by_text(combined_agent_name)).to_be_visible()