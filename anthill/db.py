from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, scoped_session, sessionmaker
from .config import get_db_url


engine = create_engine(get_db_url())
db_session = scoped_session(sessionmaker(bind=engine))


def create_tables():
    Base.metadata.create_all(bind=engine)


class Base(DeclarativeBase):
    pass
