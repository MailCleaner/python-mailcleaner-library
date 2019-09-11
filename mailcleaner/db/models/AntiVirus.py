#!/usr/bin/env python3

from mailcleaner.db import base
from mailcleaner.db.helpers import MCYesNoEnum, MCNoAddReplaceEnum
from sqlalchemy import String, Enum
from sqlalchemy.dialects.mysql import INTEGER
from . import BaseModel


class AntiVirus(base, BaseModel):
    """
    antivirus table
    """
    __tablename__ = 'antivirus'

    set_id = column(INTEGER(11), nullable=False, primary_key=True, default=1)
    scanners = column(String(120), nullable=False, default="clamav")
    scanner_timeout = column(INTEGER(11), nullable=False, default=300)
    silent = column(Enum(MCYesNoEnum), nullable=True, default=MCYesNoEnum.yes.value)
    file_timeout = column(INTEGER(11), nullable=False, default=20)
    expand_tnef = column(Enum(MCYesNoEnum), nullable=True, default=MCYesNoEnum.yes.value)
    deliver_bad_tnef = column(Enum(MCYesNoEnum), nullable=True, default=MCYesNoEnum.no.value)
    tnef_timeout = column(INTEGER(11), nullable=False, default=120)
    usetnefcontent = column(Enum(MCNoAddReplaceEnum), nullable=True, default=MCNoAddReplaceEnum.no.value)
    max_message_size = column(INTEGER(11), nullable=False, default=0)
    max_attach_size = column(INTEGER(11), nullable=False, default=-1)
    max_archive_depth = column(INTEGER(11), nullable=False, default=0)
    max_attachments_per_message = column(INTEGER(11), nullable=False, default=200)
    send_notices = column(Enum(MCYesNoEnum), nullable=True, default=MCYesNoEnum.no.value)
    notices_to = column(String(120), nullable=False, default="root")
