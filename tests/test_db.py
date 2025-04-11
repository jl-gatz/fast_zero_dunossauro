from sqlalchemy import select

from fast_zero.models import User


def test_create_user_db(session):
    user = User(
        username='dunossauro',
        email='duno@ssauro.com.br',
        password='minha-senha-aqui',
    )

    session.add(user)
    session.commit()
    result = session.scalar(
        select(User).where(User.email == 'duno@ssauro.com.br')
    )

    assert result.username == 'dunossauro'
