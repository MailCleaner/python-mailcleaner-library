#!/usr/bin/env python3

from mailcleaner.db import base
from sqlalchemy import Column, String, BLOB
from sqlalchemy.dialects.mysql import INTEGER
from . import BaseModel


class Slave(base, BaseModel):
    """
    slave table
    """
    __tablename__ = 'slave'

    id = Column(INTEGER(11), nullable=False, primary_key=True)
    hostname = Column(String(150), nullable=False, default="localhost")
    port = Column(INTEGER(11), nullable=False, default=3307)
    password = Column(String(100), nullable=True)
    ssh_pub_key = Column(BLOB, nullable=True)
