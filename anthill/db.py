from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from .config import get_db_url


engine = create_engine(get_db_url())
db_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_tables():
    Base.metadata.create_all(bind=engine)


def get_session():
    return db_session()

    
class Base(DeclarativeBase):
    pass
