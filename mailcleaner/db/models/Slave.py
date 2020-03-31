#!/usr/bin/env python3

from mailcleaner.db import base, session
from sqlalchemy import Column, Integer, String, Boolean, BLOB
from sqlalchemy import Column, String, BLOB
from sqlalchemy.dialects.mysql import INTEGER
import factory
from . import BaseModel


class Slave(base, BaseModel):
    """
    slave table
    """
    __tablename__ = 'slave'

    id = Column(INTEGER(11), nullable=False, primary_key=True)
    hostname = Column(String(150), nullable=False, default='127.0.0.1')
    port = Column(INTEGER(11), nullable=False, default=3307)
    password = Column(String(100), nullable=True, default='')
    ssh_pub_key = Column(BLOB, nullable=True)

    @classmethod
    def find_by_hostname(cls, hostname: str):
        return session.query(Slave).filter_by(hostname=hostname).first()
    
    @classmethod
    def get_all_slaves(cls):
        return session.query(Slave).all()

    @classmethod
    def get_all_hostname_slaves(cls):
        return session.query(Slave.hostname).all()

class SlaveFactory(factory.alchemy.SQLAlchemyModelFactory):
    id = factory.Sequence(lambda n: n)
    hostname = factory.Sequence(lambda n: '127.0.0.1%s' % n)
    port = 3307
    password = ''
    ssh_pub_key = ''

    class Meta:
        model = Slave
        sqlalchemy_session = session
