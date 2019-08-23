#!/usr/bin/env python3
from mailcleaner.db import base, session
from mailcleaner.db.helpers import MCBooleanStringEnum
from sqlalchemy import Column, String, BLOB, Boolean, Enum
from sqlalchemy.dialects.mysql import INTEGER
from . import BaseModel


class Administrator(base, BaseModel):
    """
    administrator table
    """
    __tablename__ = 'administrator'

    username = Column(String(120), nullable=False, unique=True)
    password = Column(String(120), nullable=False)
    can_manage_users = Column(Enum(MCBooleanStringEnum), nullable=False, default=MCBooleanStringEnum.true.value)
    can_manage_domains = Column(Enum(MCBooleanStringEnum), nullable=False, default=MCBooleanStringEnum.false.value)
    can_configure = Column(Enum(MCBooleanStringEnum), nullable=False, default=MCBooleanStringEnum.false.value)
    can_view_stats = Column(Enum(MCBooleanStringEnum), nullable=False, default=MCBooleanStringEnum.false.value)
    can_manage_host = Column(Enum(MCBooleanStringEnum), nullable=False, default=MCBooleanStringEnum.false.value)
    domains = Column(BLOB)
    allow_subdomains = Column(Enum(MCBooleanStringEnum), nullable=False, default=MCBooleanStringEnum.false.value)
    web_template = Column(String(50), nullable=False, default="default")
    id = Column(INTEGER(11), primary_key=True)

    def set_password(self, password: str) -> None:
        """
        Crypt and salt password
        :param password: password in clear
        :return: None
        """
