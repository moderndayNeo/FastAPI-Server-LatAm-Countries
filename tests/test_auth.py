import time
from fastapi.testclient import TestClient
from src.app.main import app

client = TestClient(app)

class TestAuth:
    def test_signup_login_logout(self):
        username = f"user_{int(time.time())}"
        password = "secret"

        resp = client.post("/signup", json={"username": username, "password": password})
        assert resp.status_code == 200
        data = resp.json()
        assert data["username"] == username
        assert "id" in data

        login_resp = client.post("/login", json={"username": username, "password": password})
        assert login_resp.status_code == 200
        assert login_resp.cookies.get("session")

        logout_resp = client.post("/logout")
        assert logout_resp.status_code == 200

    def test_login_wrong_password_fails(self):
        username = f"user_{int(time.time())}"
        password = "secret"

        resp = client.post("/signup", json={"username": username, "password": password})
        assert resp.status_code == 200

        bad_login = client.post("/login", json={"username": username, "password": "wrong"})
        assert bad_login.status_code == 401

