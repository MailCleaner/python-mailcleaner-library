#!/usr/bin/env python3

from mailcleaner.db import base
from mailcleaner.db.helpers import MCBooleanStringEnum
from sqlalchemy import Column, String, Enum
from sqlalchemy.dialects.mysql import INTEGER
from . import BaseModel


class Domain(base, BaseModel):
    """
    domain table
    """
    __tablename__ = 'domain'

    id = Column(INTEGER(11), nullable=False, primary_key=True)
    name = Column(String(200), nullable=False, primary_key=True, default="test.mailcleaner.net")
    active = Column(String(5), nullable=False, default="true")
    destination = Column(String(200), nullable=False, default="mail.test.mailcleaner.net")
    callout = Column(Enum(MCBooleanStringEnum), nullable=False, default=MCBooleanStringEnum.false.value)
    altcallout = Column(String(200), nullable=True)
    adcheck = Column(Enum(MCBooleanStringEnum), nullable=False, default=MCBooleanStringEnum.false.value)
    addlistcallout = Column(Enum(MCBooleanStringEnum), nullable=False, default=MCBooleanStringEnum.false.value)
    extcallout = Column(Enum(MCBooleanStringEnum), nullable=False, default=MCBooleanStringEnum.false.value)
    forward_by_mx = Column(Enum(MCBooleanStringEnum), nullable=False, default=MCBooleanStringEnum.false.value)
    greylist = Column(Enum(MCBooleanStringEnum), nullable=False, default=MCBooleanStringEnum.false.value)
    prefs = Column(INTEGER(11), nullable=False, default=1)
