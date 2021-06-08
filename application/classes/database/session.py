from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from application.settings import DATABASE
from .database import Base

def create():
    engine = create_engine(DATABASE)
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    return session
