#!/usr/bin/env python3

from mailcleaner.db import base
from sqlalchemy import Column, String, Boolean
from sqlalchemy.dialects.mysql import INTEGER
from . import BaseModel


class UserGUI(base, BaseModel):
    """
    user_gui table
    """
    __tablename__ = 'user_gui'

    set_id = Column(INTEGER(11), nullable=False, default=1)
    want_domainchooser = Column(Boolean, nullable=False, default=True)
    want_aliases = Column(Boolean, nullable=False, default=True)
    want_search = Column(Boolean, nullable=False, default=True)
    want_submit_analyse = Column(Boolean, nullable=False, default=True)
    want_reasons = Column(Boolean, nullable=False, default=True)
    want_force = Column(Boolean, nullable=False, default=True)
    want_display_user_infos = Column(Boolean, nullable=False, default=True)
    want_summary_select = Column(Boolean, nullable=False, default=True)
    want_delivery_select = Column(Boolean, nullable=False, default=True)
    want_support = Column(Boolean, nullable=False, default=True)
    want_preview = Column(Boolean, nullable=False, default=True)
    want_quarantine_bounces = Column(Boolean, nullable=False, default=True)
    default_quarantine_days = Column(INTEGER(3), nullable=False, default=7)
    default_template = Column(String(50), nullable=False, default="default")
