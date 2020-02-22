from mailcleaner.db import base, session
from sqlalchemy import Column, Integer, String, Boolean, BLOB
import factory
from . import BaseModel


class SNMPDConfig(base, BaseModel):
    """
    Slave table
    """
    __tablename__ = 'snmpd_config'

    set_id = Column(Integer, primary_key=True, nullable=False, default=1)
    allowed_ip = Column(String(200), nullable=True, default='127.0.0.1')
    community = Column(String(200), nullable=True, default='mailcleaner')
    disks = Column(String(200), nullable=True, default='/:/var')


class SlaveFactory(factory.alchemy.SQLAlchemyModelFactory):
    set_id = factory.Sequence(lambda n: n)
    hostname = factory.Sequence(lambda n: '127.0.0.1%s' % n)
    allowed_ip = factory.Sequence(lambda n: '127.0.0.1%s' % n)
    community = 'mailcleaner'
    disks = '/:/var'

    class Meta:
        model = SNMPDConfig
        sqlalchemy_session = session