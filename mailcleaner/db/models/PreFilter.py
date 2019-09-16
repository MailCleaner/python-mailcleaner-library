#!/usr/bin/env python3

from mailcleaner.db import base, session
from mailcleaner.db.helpers import MCBooleanStringEnum
from sqlalchemy import Column, String, BLOB, Boolean, Enum
from sqlalchemy.dialects.mysql import INTEGER
from . import BaseModel


class PreFilter(base, BaseModel):
    """
    prefilter table
    """
    __tablename__ = 'prefilter'

    id = Column(INTEGER(11), nullable=False, primary_key=True)
    set_id = Column(INTEGER(11), nullable=False, default=1)
    name = Column(String(200), nullable=False, primary_key=True)
    active = Column(INTEGER(1), nullable=False, default=1)
    position = Column(INTEGER(11), nullable=False, default=1)
    neg_decisive = Column(INTEGER(1), nullable=False, default=1)
    pos_decisive = Column(INTEGER(1), nullable=False, default=1)
    decisive_field = Column(String(100), nullable=False, default="none")
    timeOut = Column(INTEGER(11), nullable=False, default=10)
    maxSize = Column(INTEGER(11), nullable=False, default=500000)
    header = Column(String(200), nullable=True)
    putHamHeader = Column(INTEGER(1), nullable=False, default=0)
    putSpamHeader = Column(INTEGER(1), nullable=False, default=1)
    visible = Column(Boolean, nullable=False, default=True)
