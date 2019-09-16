#!/usr/bin/env python3

from mailcleaner.db import base
from sqlalchemy import Column, String
from sqlalchemy.dialects.mysql import INTEGER
from . import BaseModel


class MySQLAuth(base, BaseModel):
    """
    mysql_auth table
    """
    __tablename__ = 'mysql_auth'

    username = Column(String(200), nullable=False)
    domain = Column(String(50), nullable=True)
    password = Column(String(200), nullable=False)
    email = Column(String(200), nullable=False)
    realname = Column(String(200), nullable=True)
    id = Column(INTEGER(11), nullable=False, primary_key=True)
