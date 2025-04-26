from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient

from fast_zero.models import User


@pytest.mark.asyncio
async def test_get_token(client: TestClient, user: User):
    response = client.post(
        '/auth/token',
        data={'username': user.username, 'password': user.clean_password},
    )

    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert token['token_type'] == 'Bearer'
    assert 'access_token' in token


@pytest.mark.asyncio
async def test_get_token_with_wrong_user(client: TestClient, user: User):
    response = client.post(
        '/auth/token',
        data={'username': 'wrong-username', 'password': user.clean_password},
    )

    token = response.json()

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert token['detail'] == 'Incorrect username or password'


@pytest.mark.asyncio
async def test_get_token_with_wrong_password(client: TestClient, user: User):
    response = client.post(
        '/auth/token',
        data={'username': user.username, 'password': 'incorrect-password'},
    )

    token = response.json()

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert token['detail'] == 'Incorrect username or password'
