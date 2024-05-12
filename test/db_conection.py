import pytest

from database import Base
from sqlalchemy import create_engine
import os
from sqlalchemy.orm import sessionmaker

from models import Users
from routers.auth import bcrypt_context

TEST_DATABASE_URL = os.getenv('TEST_DATABASE_URL')
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="function")
def db_session():
    session = TestingSessionLocal()
    Base.metadata.create_all(bind=engine)  # Создаем все таблицы

    yield session  # Предоставляем сессию для теста

    session.close()  # Закрываем сессию после теста
    Base.metadata.drop_all(bind=engine)  # Удаляем все таблицы для очистки


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()



@pytest.fixture
def test_user(db_session):
    user = Users(
            hashed_password=bcrypt_context.hash("1234"),
            username="petrov",
            first_name="Ivan",
            last_name="Petrov",
            role="admin",
        )

    db_session.add(user)
    db_session.commit()

    yield user  # Предоставляем данные для теста

    db_session.query(Users).delete()  # Очистка тестовых данных после использования
    db_session.commit()