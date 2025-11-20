from fastapi.testclient import TestClient
from src.app import app, activities


client = TestClient(app)


def test_get_activities():
    res = client.get("/activities")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, dict)
    # Ensure an expected activity is present
    assert "Chess Club" in data


def test_signup_and_unregister_flow():
    name = "Unit Test Activity"
    email = "unit_test@example.com"

    # Prepare a clean activity for the test
    activities[name] = {
        "description": "Temp activity for tests",
        "schedule": "Now",
        "max_participants": 5,
        "participants": [],
    }

    # Sign up
    res = client.post(f"/activities/{name}/signup", params={"email": email})
    assert res.status_code == 200
    assert f"Signed up {email}" in res.json().get("message", "")
    assert email in activities[name]["participants"]

    # Unregister
    res = client.delete(f"/activities/{name}/participants", params={"email": email})
    assert res.status_code == 200
    assert f"Removed {email}" in res.json().get("message", "")
    assert email not in activities[name]["participants"]


def test_unregister_nonexistent_participant():
    name = "Unit Test Activity Nonexistent"
    activities[name] = {
        "description": "Temp",
        "schedule": "Now",
        "max_participants": 3,
        "participants": [],
    }

    res = client.delete(f"/activities/{name}/participants", params={"email": "nope@example.com"})
    assert res.status_code == 404
