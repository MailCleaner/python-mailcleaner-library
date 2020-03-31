#!/usr/bin/env python3

from mailcleaner.db import base
from mailcleaner.db.helpers import MCCountFrequency
from sqlalchemy import Column, String, Enum
from sqlalchemy.dialects.mysql import INTEGER
from . import BaseModel


class RRDStats(base, BaseModel):
    """
    rrd_stats table
    """
    __tablename__ = 'rrd_stats'

    id = Column(INTEGER(11), nullable=False, primary_key=True, default=1)
    name = Column(String(255), nullable=True)
    type = Column(Enum(MCCountFrequency), nullable=True)
    family = Column(String(255), nullable=True, default="default")
    base = Column(INTEGER(11), nullable=True, default=1)
    min_yvalue = Column(INTEGER(11), nullable=True, default=0)
