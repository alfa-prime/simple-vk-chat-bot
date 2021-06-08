from sqlalchemy import create_engine, String
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

from ..settings import DB_CONNECTION

engine = create_engine(DB_CONNECTION)
Base = declarative_base()

class Users(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True)
    vk_user_id = Column(Integer)
    name = Column(String)
    link = Column(String)

class BlackList(Base):
    __tablename__ = 'blacklist'
    black_id = Column(Integer, primary_key=True)
    target_id = Column(Integer)
    user_id = Column(Integer, ForeignKey('users.user_id'))

class WhiteList(Base):
    __tablename__ = 'whitelist'
    white_id = Column(Integer, primary_key=True)
    target_id = Column(Integer)
    user_id = Column(Integer, ForeignKey('users.user_id'))


Base.metadata.create_all(engine)
