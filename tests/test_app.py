from http import HTTPStatus

from fastapi.testclient import TestClient


def test_read_root_deve_retornar_ok_e_ola_mundo(client: TestClient):
    response = client.get('/')  # Act (ação)
    assert response.status_code == HTTPStatus.OK  # Assert
    assert response.json() == {'message': 'Olá, mundo!!'}


def test_read_root_html_deve_retornar_ok_e_tipo_html(client: TestClient):
    response = client.get('/pagina')
    assert response.status_code == HTTPStatus.OK  # Assert
    assert '<h1>Olá, crocodilo!! 🐊</h1>' in response.text
