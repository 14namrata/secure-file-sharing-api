import os
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models import SessionLocal, User
from app.utils.auth import hash_password

client = TestClient(app)

OPS_EMAIL = "ops@example.com"
OPS_PASSWORD = "securepass"

# ✅ Fixture to auto-create ops user
@pytest.fixture(scope="session", autouse=True)
def create_default_ops_user():
    db = SessionLocal()
    email = OPS_EMAIL
    password = OPS_PASSWORD
    hashed_pw = hash_password(password)

    if not db.query(User).filter_by(email=email).first():
        user = User(email=email, password=hashed_pw, role="ops", is_verified=True)
        db.add(user)
        db.commit()
    db.close()

# ✅ Helper function to get token
def get_token():
    response = client.post("/ops/login", json={
        "email": OPS_EMAIL,
        "password": OPS_PASSWORD
    })
    assert response.status_code == 200, "Login failed"
    data = response.json()
    assert "access_token" in data
    return data["access_token"]

# ✅ Tests
def test_ops_login():
    token = get_token()
    assert isinstance(token, str)

def test_upload_valid_file():
    token = get_token()
    filepath = "app/tests/sample.docx"
    try:
        # Simulate a valid DOCX file
        with open(filepath, "wb") as f:
            f.write(b"PK\x03\x04 test")

        with open(filepath, "rb") as file:
            response = client.post(
                "/ops/upload",
                headers={"Authorization": f"Bearer {token}"},
                files={"file": ("sample.docx", file, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")}
            )
    finally:
        if os.path.exists(filepath):
            os.remove(filepath)

    assert response.status_code == 200
    assert "filename" in response.json()

def test_upload_invalid_file():
    token = get_token()
    filepath = "app/tests/sample.txt"
    try:
        with open(filepath, "wb") as f:
            f.write(b"This is not a DOCX")

        with open(filepath, "rb") as file:
            response = client.post(
                "/ops/upload",
                headers={"Authorization": f"Bearer {token}"},
                files={"file": ("sample.txt", file, "text/plain")}
            )
    finally:
        if os.path.exists(filepath):
            os.remove(filepath)

    assert response.status_code == 400  # or whatever your app returns for invalid file
