from mailcleaner_db import base, session
from sqlalchemy import Column, Integer, String

from mailcleaner_db.models.BaseModel import BaseModel


class User(base, BaseModel):
    """
    User table
    """
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(120), nullable=True)
    domain = Column(String(200), nullable=True)
    pref = Column(Integer, nullable=True, default=1)

    @classmethod
    def find_by_id(cls, id: int):
        return session.query(User).filter_by(id=id).first()

    @classmethod
    def find_by_username(cls, username: str):
        return session.query(User).filter_by(username=username).all()

    @classmethod
    def find_by_domain(cls, domain: str):
        return session.query(User).filter_by(domain=domain).all()

    @classmethod
    def find_by_username_and_domain(cls, username: str, domain: str):
        return session.query(User).filter(domain == domain, username == username).first()

    @classmethod
    def find_by_pref(cls, user_pref: int):
        return session.query(User).filter_by(pref=user_pref).first()


