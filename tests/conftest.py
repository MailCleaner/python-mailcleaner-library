import pytest

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from mailcleaner.db import get_db_connection_uri

engine = create_engine(get_db_connection_uri())
Session = sessionmaker()


@pytest.fixture(scope='module')
def connection():
    connection = engine.connect()
    yield connection
    connection.close()


@pytest.fixture(scope='function')
def session(connection):
    transaction = connection.begin()
    session = Session(bind=connection)
    yield session
    session.close()
    transaction.rollback()
