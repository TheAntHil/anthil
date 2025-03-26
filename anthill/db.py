from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, scoped_session, sessionmaker
from anthill.config import create_db_url


engine = create_engine(create_db_url())
db_session = scoped_session(sessionmaker(bind=engine))


class Base(DeclarativeBase):
    pass
