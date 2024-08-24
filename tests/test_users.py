from app import schemas
from jose import jwt
import pytest
from app.config import settings


def test_create_user(client):
    response = client.post(
        "/users/", json={"email": "test_user@gmail.com", "password": "password123"}
    )
    new_user = schemas.UserRead(**response.json())
    assert response.status_code == 201
    assert new_user.email == "test_user@gmail.com"


def test_login_user(client, test_user):
    response = client.post(
        "/login", data={"username": "test_user@gmail.com", "password": "password123"}
    )
    login_res = schemas.Token(**response.json())
    payload = jwt.decode(
        login_res.access_token, settings.jwt_secret, algorithms=[settings.jwt_algorithm]
    )
    user_id = payload.get("user_id")
    assert user_id == test_user["id"]
    assert login_res.token_type == "bearer"
    assert response.status_code == 200


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("wrongemail@gmail.com", "password123", 403),
        ("nick@gmail.com", "wrongpassword", 403),
        ("wrongemail@gmail.com", "wrongpassword", 403),
        (None, "password123", 422),
        ("nick@gmail.com", None, 422),
    ],
)
def test_invalid_login(client, email, password, status_code):
    response = client.post("/login", data={"username": email, "password": password})
    assert response.status_code == status_code
