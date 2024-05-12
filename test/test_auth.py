from datetime import datetime, timedelta
from jose import jwt
from main import app
import pytest
from fastapi.testclient import TestClient
from fastapi import status, HTTPException


from models import Users
from routers.auth import get_db, authenticate_user, bcrypt_context, create_access_token, SECRET_KEY, ALGORITHM, \
    get_current_user
from test.db_conection import TestingSessionLocal, db_session, test_user, override_get_db

client = TestClient(app)
app.dependency_overrides[get_db] = override_get_db

def test_register_user(test_user, db_session):
    request_data = {
        "password": "1234",
        "username": "new-user",
        "first_name": "New",
        "last_name": "User",
        "role": "student"
    }

    response = client.post('/auth/', json=request_data)
    assert response.status_code == status.HTTP_201_CREATED

    model = db_session.query(Users).filter(Users.username == request_data['username']).one()
    assert model.first_name == request_data['first_name']
    assert model.last_name == request_data['last_name']
    assert model.role == request_data['role']


def test_register_user_empty_required_field(test_user, json=None):
    request_data = {
        "password": "1234",
        "username": "ivanov",
        "first_name": "",
        "last_name": "Ivanov",
        "role": "student"
    }

    response = client.post('/auth/', json=request_data)
    assert response.status_code == 422
    assert response.json()['detail'][0]['msg'] == 'String should have at least 2 characters'


def test_authenticate_user(test_user, db_session):

    authenticated_user = authenticate_user(test_user.username, '1234', db_session)
    assert authenticated_user is not None
    assert authenticated_user.username == test_user.username

    non_existent_user = authenticate_user('WrongUserName', 'testpassword', db_session)
    assert non_existent_user is False

    wrong_password_user = authenticate_user(test_user.username, 'wrongpassword', db_session)
    assert wrong_password_user is False


def test_create_access_token():
    username = 'testuser'
    user_id = 1
    role = 'student'
    expires_delta = timedelta(days=1)

    token = create_access_token(username, user_id, role, expires_delta)

    decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM],
                               options={'verify_signature': False})


    assert decoded_token['sub'] == username
    assert decoded_token['id'] == user_id
    assert decoded_token['role'] == role


@pytest.mark.asyncio
async def test_get_current_user_valid_token():
    encode = {'sub': 'new-user', 'id': 1, 'role': 'student'}
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    user = await get_current_user(token=token)
    assert user == {'username': 'new-user', 'id': 1, 'user_role': 'student'}


@pytest.mark.asyncio
async def test_get_current_user_missing_payload():
    encode = {'role': 'user'}
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    with pytest.raises(HTTPException) as excinfo:
        await get_current_user(token=token)

    assert excinfo.value.status_code == 401
    assert excinfo.value.detail == 'Could not validate user.'
