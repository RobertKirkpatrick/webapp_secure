import pytest
from app import app


@pytest.fixture(scope="module")
def test_client():
    app.config["WTF_CSRF_ENABLED"] = False
    t_client = app.test_client()
    yield t_client

def test_login(test_client):
    response = test_client.post(
        "/login",
        data=dict(username="bad", password="bad", two_factor="12345"),
        follow_redirects=True,
    )
    assert b"Incorrect" in response.data

def test_home(test_client):
    response = test_client.get("/")
    assert response.status_code == 302

def test_loginpost(test_client):
    response = test_client.get("/login")
    assert response.status_code == 200


def test_loginget(test_client):
    res = test_client.get("/login")
    assert res.status_code == 200


