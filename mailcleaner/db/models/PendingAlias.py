#!/usr/bin/env python3

from mailcleaner.db import base
from sqlalchemy import Column, String, Date
from . import BaseModel


class PendingAlias(base, BaseModel):
    """
    pending_alias table
    """
    __tablename__ = 'pending_alias'

    id = Column(String(32), nullable=False, primary_key=True)
    date_in = Column(Date, nullable=False)
    alias = Column(String(150), nullable=True)
    user = Column(String(150), nullable=True)
