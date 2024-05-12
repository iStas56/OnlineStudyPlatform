from routers.users import get_db, get_current_user
from fastapi.testclient import TestClient
from main import app
from fastapi import status
from test.db_conection import db_session, test_user, override_get_db


def override_get_current_user():
    return {'username': 'petrov', 'id': 1, 'user_role': 'admin'}


client = TestClient(app)

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_return_user(test_user):
    response = client.get("/user/me")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['username'] == 'petrov'
    assert response.json()['first_name'] == 'Ivan'
    assert response.json()['last_name'] == 'Petrov'
    assert response.json()['role'] == 'admin'


def test_change_password_success(test_user):
    response = client.put("/user/password", json={"password": "1234",
                                                  "new_password": "newpassword"})
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_change_password_invalid_current_password(test_user):
    response = client.put("/user/password", json={"password": "wrong_password",
                                                  "new_password": "newpassword"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'Error on password change'}