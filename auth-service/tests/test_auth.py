import pytest

# Successful Tests
def test_login_success_admin(client, test_user):
    response = client.post("/login", json={
        "username": "admin",
        "password": "admin123"
    })

    assert response.status_code == 200
    assert "access_token" in response.get_json()


def test_login_success_user(client, test_user):
    response = client.post("/login", json={
        "username": "user1",
        "password": "user123"
    })

    assert response.status_code == 200
    assert "access_token" in response.get_json()

# Failure Tests
@pytest.mark.parametrize("username,password", [
    ("admin", "wrong"),
    ("user1", "wrong"),
    ("admin1", "admin123"),
    ("user", "user123")
])
def test_login_invalid_credentials(client, username, password):
    response = client.post("/login", json={
        "username": username,
        "password": password
    })

    assert response.status_code == 401

def test_login_missing_fields(client):
    response = client.post("/login", json={})
    assert response.status_code == 400

