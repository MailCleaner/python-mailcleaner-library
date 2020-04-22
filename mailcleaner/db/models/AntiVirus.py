#!/usr/bin/env python3

from mailcleaner.db import base
from mailcleaner.db.helpers import MCYesNoEnum, MCNoAddReplaceEnum
from sqlalchemy import Column, String, Enum
from sqlalchemy.dialects.mysql import INTEGER
from . import BaseModel


class AntiVirus(base, BaseModel):
    """
    antivirus table
    """
    __tablename__ = 'antivirus'

    set_id = Column(INTEGER(11), nullable=False, primary_key=True, default=1)
    scanners = Column(String(120), nullable=False, default="clamav")
    scanner_timeout = Column(INTEGER(11), nullable=False, default=300)
    silent = Column(Enum(MCYesNoEnum),
                    nullable=True,
                    default=MCYesNoEnum.yes.value)
    file_timeout = Column(INTEGER(11), nullable=False, default=20)
    expand_tnef = Column(Enum(MCYesNoEnum),
                         nullable=True,
                         default=MCYesNoEnum.yes.value)
    deliver_bad_tnef = Column(Enum(MCYesNoEnum),
                              nullable=True,
                              default=MCYesNoEnum.no.value)
    tnef_timeout = Column(INTEGER(11), nullable=False, default=120)
    usetnefcontent = Column(Enum(MCNoAddReplaceEnum),
                            nullable=True,
                            default=MCNoAddReplaceEnum.no.value)
    max_message_size = Column(INTEGER(11), nullable=False, default=0)
    max_attach_size = Column(INTEGER(11), nullable=False, default=-1)
    max_archive_depth = Column(INTEGER(11), nullable=False, default=0)
    max_attachments_per_message = Column(INTEGER(11),
                                         nullable=False,
                                         default=200)
    send_notices = Column(Enum(MCYesNoEnum),
                          nullable=True,
                          default=MCYesNoEnum.no.value)
    notices_to = Column(String(120), nullable=False, default="root")
