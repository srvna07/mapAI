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
    

    page.submit_form()

    page.verify_success()
    page.verify_Select_Agents_to_Configure_visible()
    page.select_agent(new_organization_data["Agent"])
    page.select_model(new_organization_data["Model"], new_organization_data["Instructions"])
    page.review_and_save_agents(new_organization_data["Agent"], new_organization_data["Model"])
    page.verify_agents_update_success()
    page.verify_organization_in_table(org["name"])

def test_duplicate_organization(authenticated_page, organization_page, new_organization_data):
    page = organization_page
    org = new_organization_data["organization"]["name"]
    contact = new_organization_data["contact"]

    # Create first organization
    page.open_form()
    page.fill_basic_info(org)
    page.fill_contact_info(**contact)
    
    page.submit_form()
    page.verify_duplicate_error()

def test_search_organization(authenticated_page, organization_page, new_organization_data):
    page = organization_page
    org = new_organization_data["organization"]

    page.navigate_to_organizations()
    page.verify_organization_in_table(org["name"])


# @pytest.mark.smoke
# def test_edit_organization_verify_assigned_agents(authenticated_page, organization_page, new_organization_data):
#     page = organization_page
#     org_name = new_organization_data["organization"]["name"]

    
#     page.navigate_to_organizations()
#     # Verify assigned agents
#     page.verify_agents(org_name, new_organization_data["Agent"])
#     page.verify_models(new_organization_data["Model"])



# def test_edit_organization(authenticated_page, organization_page, new_organization_data, update_organization_data):
#     page = organization_page
#     org     = new_organization_data["organization"]["name"]
    
#     page.navigate_to_organizations()
#     page.edit_organization(org)
#     page.update_organization(update_organization_data)
#     page.select_agent(update_organization_data["Agent"]) #// Re-select same agents to remove and adding another agent#//
#     page.submit_form()
#     page.verify_update_success()

def test_delete_organization(authenticated_page, organization_page, new_organization_data):
    page = organization_page
    org = new_organization_data["organization"]

    page.navigate_to_organizations()
    page.delete_organization(org["name"])
    page.verify_delete_success()


@pytest.mark.smoke
def test_verify_all_agents_listed_in_dropdown(authenticated_page, organization_page,new_organization_data, api_client):

    page = organization_page

    # Call API using endpoint
    response = api_client.get("/api/v1/agent-temp")
    assert response.status_code == 200

    agents_api = response.json()
    agent_names = [agent["name"] for agent in agents_api]
    print("Agents from API:", agent_names)

    
    org     = new_organization_data["organization"]
    contact = new_organization_data["contact"]

    page.open_form()
    page.fill_basic_info(org["name"])
    page.fill_contact_info(**contact)
    page.submit_form()

    page.verify_success()

    page.verify_agents_in_list(agent_names)
    
    
    