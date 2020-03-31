#!/usr/bin/env python3

from mailcleaner.db import base
from sqlalchemy import Column, String
from . import BaseModel


class HTTPAuth(base, BaseModel):
    """
    http_auth table
    """
    __tablename__ = 'http_auth'

    username = Column(String(50), nullable=False, primary_key=True)
    password = Column(String(250), nullable=True)
