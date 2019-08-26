#!/usr/bin/env python3
import factory

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
    can_manage_users = Column(Boolean,
                              nullable=False,
                              default=MCBooleanStringEnum.true.value)
    can_manage_domains = Column(Boolean,
                                nullable=False,
                                default=MCBooleanStringEnum.false.value)
    can_configure = Column(Boolean,
                           nullable=False,
                           default=MCBooleanStringEnum.false.value)
    can_view_stats = Column(Boolean,
                            nullable=False,
                            default=MCBooleanStringEnum.false.value)
    can_manage_host = Column(Boolean,
                             nullable=False,
                             default=MCBooleanStringEnum.false.value)
    domains = Column(BLOB)
    allow_subdomains = Column(Boolean,
                              nullable=False,
                              default=MCBooleanStringEnum.false.value)
    web_template = Column(String(50), nullable=False, default="default")
    id = Column(INTEGER(11), primary_key=True)

    @classmethod
    def find_by_id(cls, id: int):
        return session.query(Administrator).filter_by(id=id).first()

    @classmethod
    def find_by_username(cls, username: str):
        return session.query(Administrator).filter_by(
            username=username).first()

    @classmethod
    def find_by_domain(cls, domain: str):
        return session.query(Administrator).filter(
            Administrator.domains.in_(domain)).all()

    def set_password(self, password: str) -> None:
        """
        Crypt and salt password
        :param password: password in clear
        :return: None
        """


class AdministratorFactory(factory.alchemy.SQLAlchemyModelFactory):
    id = factory.Sequence(lambda n: n)
    username = factory.Sequence(lambda n: 'toto%s' % n)
    can_manage_users = MCBooleanStringEnum.true.value
    can_manage_domains = MCBooleanStringEnum.true.value
    can_configure = MCBooleanStringEnum.true.value
    can_view_stats = MCBooleanStringEnum.true.value
    can_manage_host = MCBooleanStringEnum.true.value
    allow_subdomains = MCBooleanStringEnum.true.value
    domains = "mailcleaner.net wejob.ch lafamille.com tmtc.fr weshalors.yes b2o.oklm"

    class Meta:
        model = Administrator
        sqlalchemy_session = session
