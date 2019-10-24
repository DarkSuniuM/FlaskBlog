from sqlalchemy import Column, Integer, String
from app import db


class User(db.Model):
    id = Column(Integer(), primary_key=True)
    email = Column(String(128), nullable=False, unique=True)
    password = Column(String(128), nullable=False, unique=False)
    role = Column(Integer(), nullable=False, default=0)
    full_name = Column(String(128), nullable=True, unique=False)
