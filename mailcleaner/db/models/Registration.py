from mailcleaner.db import base, session
from mailcleaner.db.helpers import MCBooleanStringEnum
from sqlalchemy import Column, String, BLOB, Boolean, Enum
from sqlalchemy.dialects.mysql import INTEGER, TINYINT, TIMESTAMP
from . import BaseModel


class Registration(base, BaseModel):
    """
    Registration table
    """
    __tablename__ = 'registration'

    id = Column(INTEGER, primary_key=True)
    first_name = Column(String(150), nullable=False)
    last_name = Column(String(150), nullable=False)
    company = Column(String(150), nullable=False)
    email = Column(String(150), nullable=False)
    address = Column(String(150), nullable=False)
    postal_code = Column(String(150), nullable=False)
    city = Column(String(150), nullable=False)
    accept_newsletters = Column(TINYINT, nullable=False)
    accept_releases = Column(TINYINT, nullable=False)
    accept_send_statistics = Column(TINYINT, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)
    updated_at = Column(TIMESTAMP, nullable=False)

    @classmethod
    def first(cls):
        """
        Return the first row available on the table.
        :return: Model object
        """
        return session().using_bind("m_community").query(cls).first()