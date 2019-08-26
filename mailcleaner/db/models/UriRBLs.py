#!/usr/bin/env python3
import factory

from mailcleaner.db import base, session
from mailcleaner.db.helpers import MCBooleanStringEnum
from sqlalchemy import Column, String, BLOB, Boolean, Enum
from sqlalchemy.dialects.mysql import INTEGER
from . import BaseModel


class UriRBLs(base, BaseModel):
    """
    UriRBLs table
    """
    __tablename__ = 'UriRBLs'

    set_id = Column(INTEGER(11), nullable=False, primary_key=True, default=1)
    rbls = Column(String(250), nullable=True)
    listeduristobespam = Column(INTEGER(5), nullable=False, default=1)
    listedemailtobespam = Column(INTEGER(5), nullable=False, default=1)
    resolve_shorteners = Column(INTEGER(1), nullable=False, default=1)
    avoidhosts = Column(BLOB, nullable=True)


