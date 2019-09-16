#!/usr/bin/env python3

from mailcleaner.db import base
from sqlalchemy import Column, String, BLOB
from sqlalchemy.dialects.mysql import INTEGER
from . import BaseModel


class LDAPConfig(base, BaseModel):
    """
    ldapconfig table
    """
    __tablename__ = 'ldapconfig'

    id = Column(INTEGER(11), nullable=False, primary_key=True)
    name = Column(String(200), nullable=False, default="ldapconfig")
    user = Column(String(120), nullable=True)
    servers = Column(BLOB, nullable=True)
    basedb = Column(String(255), nullable=True)
    binddn = Column(String(255), nullable=True)
    bindpass = Column(String(255), nullable=True)
    user_fields = Column(String(255), nullable=True)
