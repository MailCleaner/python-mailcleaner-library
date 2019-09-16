#!/usr/bin/env python3

from mailcleaner.db import base
from sqlalchemy import Column, String, Boolean
from sqlalchemy.dialects.mysql import INTEGER
from . import BaseModel


class Scanner(base, BaseModel):
    """
    scanner table
    """
    __tablename__ = 'scanner'

    id = Column(INTEGER(11), nullable=False, primary_key=True)
    name = Column(String(40), nullable=False)
    comm_name = Column(String(40), nullable=False)
    active = Column(Boolean, nullable=False, default=False)
    path = Column(String(200), nullable=False, default="/usr/local")
    installed = Column(Boolean, nullable=False, default=False)
    version = Column(String(100), nullable=True)
    sig_version = Column(String(100), nullable=True)
