#!/usr/bin/env python3

from mailcleaner.db import base
from mailcleaner.db.helpers import MCBooleanStringEnum
from sqlalchemy import Column, String, Enum
from sqlalchemy.dialects.mysql import INTEGER
from . import BaseModel


class Email(base, BaseModel):
    """
    administrator table
    """
    __tablename__ = 'email'

    address = Column(String(120), nullable=False)
    user = Column(INTEGER(11), nullable=False, default=0)
    is_main = Column(Enum(MCBooleanStringEnum),
                     nullable=False,
                     default=MCBooleanStringEnum.true.value)
    pref = Column(INTEGER(11), nullable=False, default=1)
    id = Column(INTEGER(11), nullable=False, primary_key=True)
