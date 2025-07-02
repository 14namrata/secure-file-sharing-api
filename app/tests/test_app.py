import pytest
from fastapi.testclient import TestClient
from app.main import app



client = TestClient(app)

def test_ops_login():
    response = client.post("/ops/login", json={"username": "admin", "password": "admin123"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_client_signup():
    response = client.post("/client/signup", json={"email": "test@example.com", "password": "pass123"})
    assert response.status_code == 200
    assert "download-link" in response.json()

def test_invalid_upload():
    # Simulate wrong file type
    with open("test.txt", "rb") as f:
        response = client.post(
            "/ops/upload",
            files={"file": ("test.txt", f, "text/plain")},
            headers={"Authorization": "Bearer <valid_ops_token>"}
        )
    assert response.status_code == 400
def test_secure_download():
    login = client.post("/client/login", json={
        "email": "test@example.com",
        "password": "pass123"
    })
    token = login.json()["access_token"]
    file_id = "abc123"  # Use a real one

    response = client.get(f"/client/download/{file_id}", headers={
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code == 200
