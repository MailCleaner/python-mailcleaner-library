#!/usr/bin/env python3

from mailcleaner.db import base
from sqlalchemy import Column, BLOB
from sqlalchemy.dialects.mysql import INTEGER
from . import BaseModel


class GreylistdConfig(base, BaseModel):
    """
    greylistd_config table
    """
    __tablename__ = 'greylistd_config'

    set_id = Column(INTEGER(11), nullable=False, primary_key=True, default=1)
    retry_min = Column(INTEGER(20), nullable=False, default=120)
    retry_max = Column(INTEGER(20), nullable=False, default=28800)
    expire = Column(INTEGER(20), nullable=False, default=5184000)
    avoid_domains = Column(BLOB, nullable=True)
