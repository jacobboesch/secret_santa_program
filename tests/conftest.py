import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from secret_santa.database import Base
# must be imported so that it can create the database schema


# making the scope session ensures that it will only be ran once though the
# program. Once the program terminates it will run the code after the yield
@pytest.fixture(scope='session')
def db_connection():
    engine = create_engine("sqlite:///:memory:", convert_unicode=True)
    Base.metadata.bind = engine
    import secret_santa.model
    Base.metadata.create_all(bind=engine)
    connection = engine.connect()

    yield connection
    # code after yeild serves as tear down
    Base.metadata.drop_all()

# socpe is modual so it runs once per unit test file
@pytest.fixture(scope="module")
def session(db_connection):
    transaction = db_connection.begin()
    session = scoped_session(sessionmaker(autocommit=False,
                                          autoflush=False,
                                          bind=db_connection))

    yield session

    transaction.rollback()
    session.close()
