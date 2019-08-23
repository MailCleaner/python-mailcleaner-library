#!/usr/bin/env python3
from mailcleaner.db import base, session
from sqlalchemy import Column, Integer, String

from mailcleaner.db.models import BaseModel


class Commtouch(base, BaseModel):
    """
    User table
    """
    __tablename__ = 'Commtouch'

    set_id = Column(Integer, primary_key=True, default=1)
    ctasdLicense = Column(String(250), nullable=True)
    ctipdLicense = Column(String(200), nullable=True)
