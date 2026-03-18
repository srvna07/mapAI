import pytest


USER_PREFIX = "test_"
ORG_PREFIX  = "test_"


def delete_all(api_client, fetch_endpoint, delete_endpoint, id_field, name_field, prefix, label):
    print(f"\n--- {label} ---")

    response = api_client.get(fetch_endpoint, params={"pageNumber": 1, "pageSize": 1000})
    assert response.status_code == 200, f"Failed to fetch {label}"

    data = response.json()
    records = data if isinstance(data, list) else data.get("data", [])

    items = []
    for i in records:
        name_value = str(i.get(name_field, ""))
        if name_value.startswith(prefix):
            items.append(i)

    print(f"Found {len(items)} test {label}")

    if not items:
        print(f"No test {label} to delete.")
        return

    deleted, failed = 0, 0

    for item in items:
        item_id = item.get(id_field)
        name_value = item.get(name_field)

        if not str(name_value).startswith(prefix):
            print(f"[SKIPPED] Not a test record: {name_value}")
            continue

        endpoint = delete_endpoint.format(id=item_id)
        res = api_client.delete(endpoint)

        
        if res.status_code == 200:
            print(f"[OK] Deleted {name_value} (ID: {item_id})")
            deleted += 1
        else:
            print(f"[ERROR] Failed {name_value} (ID: {item_id}) → {res.status_code}")
            failed += 1

    print(f"[SUMMARY] {label} — Deleted: {deleted}, Failed: {failed}")



def test_cleanup_test_data(authenticated_page,api_client):

    delete_all(
        api_client,
        fetch_endpoint="/api/v1/users",
        delete_endpoint="/api/v1/users/{id}",
        id_field="id",
        name_field="firstName",
        prefix=USER_PREFIX,
        label="Users"
    )

    delete_all(
        api_client,
        fetch_endpoint="/api/v1/organization",
        delete_endpoint="/api/v1/organization/{id}",
        id_field="id",
        name_field="organizationName",
        prefix=ORG_PREFIX,
        label="Organizations"
    )