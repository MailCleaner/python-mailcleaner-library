#!/usr/bin/env python3

from mailcleaner.db import base
from mailcleaner.db.helpers import MCTCPEnum
from sqlalchemy import Column, String, BLOB, Enum
from sqlalchemy.dialects.mysql import INTEGER
from . import BaseModel


class ExternalAccess(base, BaseModel):
    """
    external_access table
    """
    __tablename__ = 'external_access'

    id = Column(INTEGER(11), nullable=False, primary_key=True)
    service = Column(String(20), nullable=False)
    port = Column(String(20), nullable=True)
    protocol = Column(Enum(MCTCPEnum), nullable=True)
    allowed_ip = Column(BLOB, nullable=True)
    auth = Column(BLOB, nullable=True)
