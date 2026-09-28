import os


os.environ["DATABASE_URL"] = (
    "sqlite:///./test_pocketsmart.db"
)

os.environ["MOCK_MODE"] = "true"

os.environ["SECRET_KEY"] = (
    "test-secret"
)


from fastapi.testclient import (
    TestClient
)

from app.main import app


client = TestClient(
    app
)


def test_health():

    response = client.get(
        "/health"
    )

    assert response.status_code == 200

    assert response.json()[
        "status"
    ] == "ok"


def test_register_login_and_home():

    email = (
        "test@example.com"
    )

    response = client.post(
        "/register",
        json={
            "name": "Test User",
            "email": email,
            "password": "password123",
        },
    )

    assert response.status_code in (
        200,
        409,
    )


    response = client.post(
        "/login",
        json={
            "email": email,
            "password": "password123",
        },
    )

    assert response.status_code == 200


    response = client.post(
        "/generate-home",
        json={
            "budget": 50000,
            "room": "Living Room",
            "style": "Modern",
            "items": (
                "Sofa, lights, storage"
            ),
            "notes": "",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert "history_id" in body

    assert (
        body["result"]["total_budget"]
        == 50000
    )