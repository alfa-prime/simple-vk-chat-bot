from sqlalchemy import create_engine, String
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

from ..settings import DB_CONNECTION
from ..utilites.logger import set_logger

logger = set_logger(__name__)

try:
    engine = create_engine(DB_CONNECTION)
    Base = declarative_base()
except AttributeError as error:
    error_message = 'Не указана строка подключения базы данных'
    print(error_message)
    logger.error(error_message)
    exit()

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
    id = Column(Integer)
    name = Column(String)
    link = Column(String)
    bdate = Column(String)
    user_id = Column(Integer, ForeignKey('users.user_id'))


Base.metadata.create_all(engine)
