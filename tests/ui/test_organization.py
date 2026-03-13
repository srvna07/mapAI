import pytest
from utils.api_client import APIClient

@pytest.mark.smoke
def test_create_organization(authenticated_page, organization_page, new_organization_data):
    page    = organization_page
    org     = new_organization_data["organization"]
    contact = new_organization_data["contact"]

    page.open_form()
    page.fill_basic_info(org["name"])
    page.fill_contact_info(**contact)
    page.select_agent(new_organization_data["Agent"])

    
    page.submit_form()

    page.verify_success()

def test_duplicate_organization(authenticated_page, organization_page, new_organization_data):
    page = organization_page
    org = new_organization_data["organization"]
    contact = new_organization_data["contact"]

    # Create first organization
    page.open_form()
    page.fill_basic_info(org["name"])
    page.fill_contact_info(**contact)
    page.select_agent(new_organization_data["Agent"])
    page.submit_form()
    page.verify_duplicate_error()

@pytest.mark.smoke
def test_edit_organization_verify_assigned_agents(authenticated_page, organization_page, new_organization_data):
    page = organization_page
    org = new_organization_data["organization"]

    
    page.navigate_to_organizations()

    # Edit and verify agents
    page.edit_organization(org["name"])
    # Verify assigned agents
    page.verify_agents(new_organization_data["Agent"])

def test_search_organization(authenticated_page, organization_page, new_organization_data):
    page = organization_page
    org = new_organization_data["organization"]

    page.navigate_to_organizations()
    page.verify_organization_in_table(org["name"])


def test_edit_organization(authenticated_page, organization_page, update_organization_data):
    page = organization_page
    org     = update_organization_data["organization"]
    contact = update_organization_data["contact"]

    page.navigate_to_organizations()
    page.edit_organization(org["name"])
    page.update_organization(update_organization_data)
    page.select_agent(update_organization_data["Agent"]) #// Re-select same agents to remove and adding another agent#//
    page.submit_form()
    page.verify_update_success()

def test_delete_organization(authenticated_page, organization_page, update_organization_data):
    page = organization_page
    org = update_organization_data["organization"]

    page.navigate_to_organizations()
    page.delete_organization(org["name"])
    page.verify_delete_success()


@pytest.mark.smoke
def test_verify_all_agents_listed_in_dropdown(authenticated_page, organization_page, api_client: APIClient):

    page = organization_page

    # Call API using endpoint
    response = api_client.get("/api/v1/agents/all")
    assert response.status_code == 200

    agents_api = response.json()
    agent_names = [agent["name"] for agent in agents_api["data"]]

    page.navigate_to_organizations()
    page.open_form()
    page.open_agent_dropdown()

    page.verify_agents(agent_names)
    
    
    
    