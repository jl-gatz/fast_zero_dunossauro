from dataclasses import asdict

import pytest
from sqlalchemy import select

from fast_zero.models import User


@pytest.mark.asyncio
async def test_create_user_db(session):
    user = User(
        username='alice',
        email='alice@ssauro.com.br',
        password='minha-senha-aqui',
    )

    session.add(user)
    await session.commit()
    result = await session.scalar(
        select(User).where(User.email == 'alice@ssauro.com.br')
    )

    assert result.username == 'alice'


@pytest.mark.asyncio
async def test_create_user_db_with_time(session, mock_db_time):
    with mock_db_time(model=User) as time:
        new_user = User(
            username='arisu', password='secret', email='teste@test'
        )
        session.add(new_user)
        await session.commit()

        user = await session.scalar(
            select(User).where(User.username == 'arisu')
        )

    assert asdict(user) == {
        'id': 1,
        'username': 'arisu',
        'password': 'secret',
        'email': 'teste@test',
        'created_at': time,
        'updated_at': time,
    }
