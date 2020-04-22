#!/usr/bin/env python3

from mailcleaner.db import base, session
from mailcleaner.db.helpers import MCBooleanStringEnum
from sqlalchemy import Column, String, BLOB, Boolean, Enum
from sqlalchemy.dialects.mysql import INTEGER
from . import BaseModel


class SNMPDConfig(base, BaseModel):
    """
    snmpd_config table
    """
    __tablename__ = 'snmpd_config'
    set_id = Column(INTEGER(11), nullable=False, primary_key=True, default=1)
    allowed_ip = Column(String(200), nullable=True, default="127.0.0.1")
    community = Column(String(200), nullable=True, default="mailcleaner")
    disks = Column(String(200), nullable=True, default="/:/var")
