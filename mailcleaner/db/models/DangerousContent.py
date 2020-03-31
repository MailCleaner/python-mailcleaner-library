#!/usr/bin/env python3

from mailcleaner.db import base
from mailcleaner.db.helpers import MCYesNoEnum, MCYesNoDisarmEnum
from sqlalchemy import Column, BLOB, Boolean, Enum
from sqlalchemy.dialects.mysql import INTEGER
from . import BaseModel


class DangerousContent(base, BaseModel):
    """
    dangerouscontent table
    """
    __tablename__ = 'dangerouscontent'

    set_id = Column(INTEGER(11), nullable=False, primary_key=True, default=1)
    block_encrypt = Column(Enum(MCYesNoEnum), nullable=True, default=MCYesNoEnum.no.value)
    block_unencrypt = Column(Enum(MCYesNoEnum), nullable=True, default=MCYesNoEnum.no.value)
    allow_passwd_archives = Column(Enum(MCYesNoEnum), nullable=True, default=MCYesNoEnum.no.value)
    allow_partial = Column(Enum(MCYesNoEnum), nullable=True, default=MCYesNoEnum.no.value)
    allow_external_bodies = Column(Enum(MCYesNoEnum), nullable=True, default=MCYesNoEnum.no.value)
    allow_iframe = Column(Enum(MCYesNoDisarmEnum), nullable=True, default=MCYesNoDisarmEnum.no.value)
    silent_iframe = Column(Enum(MCYesNoEnum), nullable=True, default=MCYesNoEnum.yes.value)
    allow_form = Column(Enum(MCYesNoDisarmEnum), nullable=True, default=MCYesNoDisarmEnum.yes.value)
    silent_form = Column(Enum(MCYesNoEnum), nullable=True, default=MCYesNoEnum.no.value)
    allow_script = Column(Enum(MCYesNoDisarmEnum), nullable=True, default=MCYesNoDisarmEnum.yes.value)
    silent_script = Column(Enum(MCYesNoEnum), nullable=True, default=MCYesNoEnum.no.value)
    allow_webbugs = Column(Enum(MCYesNoDisarmEnum), nullable=True, default=MCYesNoDisarmEnum.disarm.value)
    silent_webbugs = Column(Enum(MCYesNoEnum), nullable=True, default=MCYesNoEnum.no.value)
    allow_codebase = Column(Enum(MCYesNoDisarmEnum), nullable=True, default=MCYesNoDisarmEnum.no.value)
    silent_codebase = Column(Enum(MCYesNoEnum), nullable=True, default=MCYesNoEnum.no.value)
    notify_sender = Column(Enum(MCYesNoEnum), nullable=True, default=MCYesNoEnum.no.value)
    wh_passwd_archives = Column(BLOB, nullable=True)
