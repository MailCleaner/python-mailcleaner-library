#!/usr/bin/env python3
from mailcleaner.db import base, session
from sqlalchemy import Column, Integer, String, Boolean
from . import BaseModel

routing_session = ""


class Fail2banJail(base, BaseModel):
    """
    Fail2banJail table
    """
    __tablename__ = 'fail2ban_jail'

    id = Column(Integer, primary_key=True)
    enabled = Column(Boolean, nullable=True, default=True)
    name = Column(String(150), nullable=False, unique=True)
    maxretry = Column(Integer, nullable=False)
    findtime = Column(Integer, nullable=False)
    bantime = Column(Integer, nullable=False)
    port = Column(String(50), nullable=False)
    filter = Column(String(50), nullable=False)
    banaction = Column(String(50), nullable=False)
    logpath = Column(String(250), nullable=False)
    max_count = Column(Integer, nullable=False)
    send_mail = Column(Boolean, nullable=True, default=False)
    send_mail_bl = Column(Boolean, nullable=True, default=True)

    @classmethod
    def find_by_id(cls, id: int):
        return session.query(Fail2banJail).filter_by(id=id).first()

    @classmethod
    def find_by_name(cls, name: str):
        return session.query(Fail2banJail).filter_by(name=name).first()

    @classmethod
    def get_jails(cls):
        return session.query(Fail2banJail.name).distinct(
            Fail2banJail.name).all()