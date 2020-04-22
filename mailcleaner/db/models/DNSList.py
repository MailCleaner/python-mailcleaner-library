#!/usr/bin/env python3

from mailcleaner.db import base
from sqlalchemy import Column, String, BLOB, Boolean
from . import BaseModel


class DNSList(base, BaseModel):
    """
    dnslist table
    """
    __tablename__ = 'dnslist'

    name = Column(String(40), nullable=False, primary_key=True)
    url = Column(String(250), nullable=False)
    type = Column(String(20), nullable=False, default="blacklist")
    active = Column(Boolean, nullable=False, default=True)
    comment = Column(BLOB, nullable=True)
