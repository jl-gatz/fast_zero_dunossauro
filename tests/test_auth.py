from http import HTTPStatus

from fastapi.testclient import TestClient

from fast_zero.models import User


def test_get_token(client: TestClient, user: User):
    response = client.post(
        '/auth/token',
        data={'username': user.username, 'password': user.clean_password},
    )

    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert token['token_type'] == 'Bearer'
    assert 'access_token' in token


def test_get_token_with_wrong_user(client: TestClient, user: User):
    response = client.post(
        '/auth/token',
        data={'username': 'wrong-username', 'password': user.clean_password},
    )

    token = response.json()

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert token['detail'] == 'Incorrect username or password'


def test_get_token_with_wrong_password(client: TestClient, user: User):
    response = client.post(
        '/auth/token',
        data={'username': user.username, 'password': 'incorrect-password'},
    )

    token = response.json()

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert token['detail'] == 'Incorrect username or password'
