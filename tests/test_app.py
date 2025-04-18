from http import HTTPStatus

from fast_zero.schemas import UserPublic


def test_read_root_deve_retornar_ok_e_ola_mundo(client):
    response = client.get('/')  # Act (ação)
    assert response.status_code == HTTPStatus.OK  # Assert
    assert response.json() == {'message': 'Olá, mundo!!'}


def test_read_root_html_deve_retornar_ok_e_tipo_html(client):
    response = client.get('/pagina')
    assert response.status_code == HTTPStatus.OK  # Assert
    assert '<h1>Olá, crocodilo!! 🐊</h1>' in response.text


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'test-user',
            'password': 'password',
            'email': 'teste@test.com',
        },
    )

    # Validar UserPublic
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'test-user',
        'email': 'teste@test.com',
        'id': 1,
    }


def test_create_user_with_existing_username_error_400(client, user):
    response = client.post(
        '/users/',
        json={
            'username': user.username,
            'email': 'rolando@lero.com',
            'password': 'amado-mestre',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Username already exists'}


def test_create_user_with_existing_email_error_400(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'Rolando Lero',
            'email': user.email,
            'password': 'amado-mestre',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Email already exists'}


def test_read_users_void(client):
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_users_with_user(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_read_user_by_id(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == user_schema


def test_read_user_by_id_user_not_found(client):
    response = client.get('/users/666')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_update_users(client, user):
    response = client.put(
        'users/1',
        json={
            'username': 'test-user2',
            'password': 'password',
            'email': 'teste@test.com',
        },
    )
    assert response.json() == {
        'id': 1,
        'username': 'test-user2',
        'email': 'teste@test.com',
    }


def test_update_users_user_not_found(client):
    response = client.put(
        'users/666',
        json={
            'username': 'test-user-quevedo',
            'password': 'isso-non-ecziste',
            'email': 'email@existe.com',
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_delete_user(client, user):
    response = client.delete('/users/1')
    assert response.json() == {'message': 'User deleted'}


def test_delete_user_user_not_found(client):
    response = client.delete('/users/666')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}
