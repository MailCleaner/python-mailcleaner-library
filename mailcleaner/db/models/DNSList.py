#!/usr/bin/env python3

from mailcleaner.db import base, session
from sqlalchemy import Column, String, BLOB, Boolean, Enum
from sqlalchemy.dialects.mysql import INTEGER
from . import BaseModel


class DNSList(base, BaseModel):
    """
    dnslist table
    """
    __tablename__ = 'dnslist'

    name = Column(String(40), nullable=Flase, primary_key=True)
    url = Column(String(250), nullable=Flase)
    type = Column(String(20), nullable=Flase, default="blacklist")
    active = Column(Boolean, nullable=Flase, default=True)
    comment = Column(BLOB, nullable=True)
