from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

# Create an engine from environment.
connection_string = os.environ.get("SECRET_SANTA_DB_CONNECTION_STRING")
engine = create_engine(connection_string, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

# Create a declarative context
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    import secret_santa.model
    Base.metadata.create_all(bind=engine)
    engine.connect()
