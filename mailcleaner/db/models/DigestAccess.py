#!/usr/bin/env python3

from mailcleaner.db import base
from sqlalchemy import Column, String, Date
from . import BaseModel


class DigestAccess(base, BaseModel):
    """
    digest_access table
    """
    __tablename__ = 'digest_access'

    id = Column(String(40), nullable=False, primary_key=True)
    date_in = Column(Date, nullable=False)
    date_start = Column(Date, nullable=False)
    date_expire = Column(Date, nullable=False)
    address = Column(String(250), nullable=False)
