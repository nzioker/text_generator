from fastapi.testclient import TestClient
from app.main import app
import pytest

client = TestClient(app)

def test_signup():
    details = {
        "names":"James10",
        "email":"james10@gmail.com",
        "password":"3rillianT.me"
    }
    response = client.post("/signup", json=details)
    assert "User registered succesfully." in response.text
    assert response.status_code == 201


def test_login():
    details = {
        "names":"James9",
        "email":"james9@gmail.com",
        "password":"3rillianT.me"
    }
    response = client.post("/signup", json=details)

    details = {
        "names":"james9",
        "email":"james9@gmail.com",
        "password":"3rillianT.me"
    }
    response = client.post("/login", json=details)

    assert "Login succesfull" in response.text
    assert response.status_code == 200