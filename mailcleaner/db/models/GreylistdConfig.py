#!/usr/bin/env python3
from mailcleaner.db import base, session
from sqlalchemy import Column, String, BLOB, Boolean
from sqlalchemy.dialects.mysql import INTEGER
from . import BaseModel


class GreylistdConfig(base, BaseModel):
    """
    httpd_config table
    @TODO: - verify that every property fits correctly the table structure
    """
    __tablename__ = 'greylistd_config'

    set_id = Column(INTEGER(11), primary_key=True, default=1)
    retry_min = Column(INTEGER(20), nullable=False, default=120)
    retry_max = Column(INTEGER(20), nullable=False, default=28800)
    expire = Column(INTEGER(20), nullable=False, default=5184000)
    avoid_domains = Column(BLOB, nullable=True, default=None)


class GreylistdConfigFactory(factory.alchemy.SQLAlchemyModelFactory):
    id = factory.Sequence(lambda n: n)
    hostname = factory.Sequence(lambda n: '127.0.0.1%s' % n)
    port = 3307
    set_id = factory.Sequence(lambda n: n)
    retry_min = 120
    retry_max = 28800
    expire = 5184000
    avoid_domains = None

    class Meta:
        model = GreylistdConfig
        sqlalchemy_session = session