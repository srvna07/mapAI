import pytest

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
