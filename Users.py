
from flask import Flask,request
import time
import datetime
import threading
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, Index
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine
from sqlalchemy.sql import text

Base = declarative_base()


class Users(Base):
    __tablename__ = 'users'


    id = Column(Integer, primary_key=True)
    name = Column(String(32), index=True)
    age = Column(Integer, default=18)
    address = Column(String(32), unique=True)
    tel = Column(Integer, unique=True)
    ctime = Column(DateTime, default=datetime.datetime.now)

    __table_args__ = (
        # UniqueConstraint('id', 'name', name='uix_id_name'),
        # Index('ix_id_name', 'name', 'email'),
    )
