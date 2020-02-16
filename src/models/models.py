from datetime import datetime, timedelta

from sqlalchemy import Column, Integer, String, Date, Boolean, create_engine, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///database.db")
session = sessionmaker(bind=engine)()
Base = declarative_base()


# https://docs.sqlalchemy.org/en/13/orm/tutorial.html
# Base.metadata.create_all(engine)


class Ban(Base):
    __tablename__ = 'bans'

    id = Column(Integer, primary_key=True)

    target_id = Column(Integer)
    author_id = Column(Integer)
    is_active = Column(Boolean, default=True)
    reason = Column(String)
    date = Column(DateTime, default=datetime.now())

    def __init__(self, target_id: int, author_id: int, reason: str):
        self.target_id = target_id
        self.author_id = author_id
        self.is_active = True
        self.reason = reason


class Kick(Base):
    __tablename__ = 'kicks'

    id = Column(Integer, primary_key=True)

    target_id = Column(Integer)
    author_id = Column(Integer)
    is_active = Column(Boolean, default=True)
    reason = Column(String)
    date = Column(DateTime, default=datetime.now())

    def __init__(self, target_id: int, author_id: int, reason: str):
        self.target_id = target_id
        self.author_id = author_id
        self.is_active = True
        self.reason = reason


class Warn(Base):
    __tablename__ = 'warns'

    id = Column(Integer, primary_key=True)

    target_id = Column(Integer)
    author_id = Column(Integer)
    is_active = Column(Boolean, default=True)
    reason = Column(String)
    date = Column(DateTime, default=datetime.now())

    def __init__(self, target_id: int, author_id: int, reason: str):
        self.target_id = target_id
        self.author_id = author_id
        self.is_active = True
        self.reason = reason


class Mute(Base):
    __tablename__ = 'mutes'

    id = Column(Integer, primary_key=True)

    target_id = Column(Integer)
    author_id = Column(Integer)
    is_active = Column(Boolean, default=True)
    reason = Column(String)
    start_time = Column(DateTime, default=datetime.now())
    end_time = Column(DateTime)

    def __init__(self, target_id: int, author_id: int, reason: str, duration: int):
        self.target_id = target_id
        self.author_id = author_id
        self.is_active = True
        self.reason = reason
        self.end_time = datetime.now() + timedelta(minutes=duration)


class CustomCommand(Base):
    __tablename__ = 'customCommands'

    id = Column(Integer, primary_key=True)
    command = Column(String)
    content = Column(String)

    def __init__(self, command: str, content: str):
        self.command = command
        self.content = content
