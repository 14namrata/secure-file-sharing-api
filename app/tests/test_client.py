from fastapi.testclient import TestClient
from app.main import app
import os
from docx import Document

client = TestClient(app)

CLIENT_EMAIL = "test@example.com"
CLIENT_PASSWORD = "pass123"
TOKEN = None

def test_client_signup():
    response = client.post("/client/signup", json={
        "email": CLIENT_EMAIL,
        "password": CLIENT_PASSWORD
    })
    assert response.status_code in [200, 400]

def test_client_login():
    response = client.post("/client/login", json={
        "email": CLIENT_EMAIL,
        "password": CLIENT_PASSWORD
    })
    assert response.status_code == 200
    global TOKEN
    TOKEN = response.json()["access_token"]

def test_list_files():
    headers = {"Authorization": f"Bearer {TOKEN}"}
    response = client.get("/client/files", headers=headers)
    assert response.status_code in [200, 404]

def create_test_docx(filename="test_file.docx"):
    doc = Document()
    doc.add_paragraph("This is a test DOCX file.")
    doc.save(filename)

def test_download_link():
    headers = {"Authorization": f"Bearer {TOKEN}"}
    create_test_docx()

    with open("test_file.docx", "rb") as f:
        upload_response = client.post(
            "/ops/upload",
            files={"file": ("test_file.docx", f, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")},
            headers=headers
        )

    os.remove("test_file.docx")
    assert upload_response.status_code == 200
    file_id = upload_response.json()["file_id"]
    response = client.get(f"/client/download/{file_id}", headers=headers)
    assert response.status_code == 200

def test_secure_download():
    headers = {"Authorization": f"Bearer {TOKEN}"}
    create_test_docx()

    with open("test_file.docx", "rb") as f:
        upload_response = client.post(
            "/ops/upload",
            files={"file": ("test_file.docx", f, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")},
            headers=headers
        )

    os.remove("test_file.docx")
    assert upload_response.status_code == 200
    file_id = upload_response.json()["file_id"]
    response = client.get(f"/client/download/{file_id}", headers=headers)
    assert response.status_code == 200
