#!/usr/bin/env python3
from mailcleaner.db import base, session
from sqlalchemy import Column, Integer, String, Date, BLOB

from . import BaseModel


class WWLists(base, BaseModel):
    """
    WWLists table
    """
    __tablename__ = 'wwlists'

    id = Column(Integer, primary_key=True)
    sender = Column(String(150), nullable=False)
    recipient = Column(String(150), nullable=False)
    type = Column(String(15), nullable=False)
    expiracy = Column(Date, nullable=False)
    status = Column(Integer, default=1)
    comments = Column(BLOB)

    @classmethod
    def find_by_sender(cls, sender: str):
        return session.query(WWLists).filter_by(sender=sender).all()

    @classmethod
    def find_by_recipient(cls, recipient: str):
        return session.query(WWLists).filter_by(recipient=recipient).all()

    @classmethod
    def find_by_type(cls, type: str):
        return session.query(WWLists).filter_by(type=type).all()

    @classmethod
    def find_by_comments(cls, comments: str):
        return session.query(WWLists).filter_by(comments=comments).all()

    @classmethod
    def find_by_sender_and_recipient(cls, sender: str, recipient: str):
        return session.query(WWLists).filter(sender == sender,
                                             recipient == recipient).first()

    @classmethod
    def find_by_sender_and_recipient_and_type(cls, sender: str, recipient: str,
                                              type: str):
        return session.query(WWLists).filter(sender == sender,
                                             recipient == recipient,
                                             type == type).first()
