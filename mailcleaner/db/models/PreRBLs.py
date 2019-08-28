#!/usr/bin/env python3
import factory

from mailcleaner.db import base, session
from mailcleaner.db.helpers import MCBooleanStringEnum
from sqlalchemy import Column, String, BLOB, Boolean, Enum
from sqlalchemy.dialects.mysql import INTEGER
from . import BaseModel


class PreRBLs(base, BaseModel):
    """
    PreRBLs table
    """
    __tablename__ = 'PreRBLs'

    set_id = Column(INTEGER(11), nullable=False, primary_key=True, default=1)
    spamhits = Column(INTEGER(5), nullable=False, default=2)
    highspamhits = Column(INTEGER(5), nullable=False, default=3)
    lists = Column(String(255), nullable=True, default="SPAMHAUS-ZEN spamcop.net NJABL SORBS-DNSBL")
    avoidgoodspf = Column(INTEGER(1), nullable=False, default=0)
    avoidhosts = Column(BLOB, nullable=True)

