#!/usr/bin/env python3

from mailcleaner.db import base
from mailcleaner.db.helpers import MCAdminManagerHotlineEnum
from sqlalchemy import Column, String, Boolean, Enum
from sqlalchemy.dialects.mysql import INTEGER
from . import BaseModel


class FeatureRestriction(base, BaseModel):
    """
    feature_restriction table
    """
    __tablename__ = 'feature_restriction'

    id = Column(INTEGER(11), nullable=False, primary_key=True)
    section = Column(String(120), nullable=False)
    feature = Column(String(120), nullable=False)
    target_level = Column(Enum(MCAdminManagerHotlineEnum), nullable=True)
    restricted = Column(Boolean, nullable=False, default=False)
