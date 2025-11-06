import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_register_and_login():
    # register
    resp = client.post("/auth/register", json={"email":"testuser@example.com","password":"password123","full_name":"Tester","role":"responder"})
    assert resp.status_code == 200
    body = resp.json()
    assert "id" in body

    # login
    resp2 = client.post("/auth/token", data={"username":"testuser@example.com","password":"password123"})
    assert resp2.status_code == 200
    token = resp2.json().get("access_token")
    assert token
