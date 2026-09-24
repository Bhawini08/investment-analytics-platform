from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from .config import settings

class Base(DeclarativeBase):
    pass

def make_engine(url=None):
    return create_engine(url or settings.database_url,future=True)

def make_session_factory(url=None):
    engine=make_engine(url)
    return engine,sessionmaker(bind=engine,expire_on_commit=False,future=True)
