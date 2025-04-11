import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from fast_zero.models import table_registry
from src.fast_zero.app import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def session():
    engine = create_engine('sqlite:///:memory:')
    table_registry.metadata.create_all(engine)

    # yield session
    with Session(engine) as session:
        yield session

    # Após a session --> tear_down()
    table_registry.metadata.drop_all(engine)
