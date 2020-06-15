from mailcleaner.db import base, session
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, UniqueConstraint
from sqlalchemy.sql import func
import factory
from . import BaseModel


class Fail2banConfig(base, BaseModel):
    __tablename__ = 'fail2ban_conf'

    id = Column(Integer, primary_key=True)
    src_email = Column(String(150), nullable=False)
    src_name = Column(String(150), nullable=False)
    dest_email = Column(String(150), nullable=True, default=True)