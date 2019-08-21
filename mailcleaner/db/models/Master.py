from mailcleaner.db import base, session
from sqlalchemy import Column, Integer, String, Boolean, BLOB

from . import BaseModel


class Master(base, BaseModel):
    """
    Master table
    """
    __tablename__ = 'master'

    hostname = Column(String(150), primary_key=True, default='localhost')
    port = Column(Integer, nullable=False, default=3306)
    password = Column(String(100), nullable=True, default='')
    ssh_pub_key = Column(BLOB, nullable=True)