#!/usr/bin/env python3

from mailcleaner.db import base
from mailcleaner.db.helpers import MCAllowDenyEnum
from sqlalchemy import Column, String, Enum
from sqlalchemy.dialects.mysql import INTEGER
from . import BaseModel


class FileType(base, BaseModel):
    """
    filetype table
    """
    __tablename__ = 'filetype'

    id = Column(INTEGER(11), nullable=False, primary_key=True)
    status = Column(Enum(MCAllowDenyEnum), nullable=True, default=MCAllowDenyEnum.allow.value)
    type = Column(String(50), nullable=False)
    name = Column(String(150), nullable=True)
    description = Column(String(150), nullable=True)
