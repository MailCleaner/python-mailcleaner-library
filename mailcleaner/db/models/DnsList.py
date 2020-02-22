#!/usr/bin/env python3
from mailcleaner.db import base, session
from sqlalchemy import Column, String, BLOB, Boolean
from sqlalchemy.dialects.mysql import INTEGER, TINYINT
from . import BaseModel


class DnsList(base, BaseModel):
    """
    httpd_config table
    @TODO: - verify that every property fits correctly the table structure
    """
    __tablename__ = 'dnslist'
    name = Column(String(40), nullable=False, primary_key=True)
    url = Column(String(250), nullable=False)
    type = Column(String(20), nullable=False)
    active = Column(TINYINT(1), nullable=False)
    comment = Column(BLOB, nullable=True, default=None)

    @classmethod
    def get_all_name(self):
        return session.query(Fail2banJail.name).all()