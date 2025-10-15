import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

def test_signup_activity():
    # Use a test activity and email
    activity = list(client.get("/activities").json().keys())[0]
    email = "testuser@example.com"
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code in (200, 400)  # 400 if already signed up

def test_duplicate_signup():
    activity = list(client.get("/activities").json().keys())[0]
    email = "testuser@example.com"
    # First signup
    client.post(f"/activities/{activity}/signup?email={email}")
    # Second signup should fail
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 400
    assert "already signed up" in response.json().get("detail", "")
