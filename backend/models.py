from sqlalchemy import Column, Integer,DateTime,String
from .database import Base
from datetime import datetime


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    password = Column(String)


# for tracker

class TaskLog(Base):
    __tablename__ = "task_logs"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(String)
    time = Column(String)
    task = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
