#!/usr/bin/env python3

from mailcleaner.db import base
from sqlalchemy import Column, String
from sqlalchemy.dialects.mysql import INTEGER
from . import BaseModel


class MessageSniffer(base, BaseModel):
    """
    MessageSniffer table
    """
    __tablename__ = 'MessageSniffer'

    set_id = Column(INTEGER(11), nullable=False, primary_key=True, default=1)
    licenseid = Column(String(255), nullable=True)
    authentication = Column(String(255), nullable=True)
