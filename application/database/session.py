from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..settings import DB_CONNECTION
from .database import Base

def create():
    engine = create_engine(DB_CONNECTION)
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    return session
