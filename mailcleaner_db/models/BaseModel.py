from mailcleaner_db import base, session


class BaseModel(object):
    """
    Base Model for creating a MailCleaner Model related to a table of mc_config db.
    Every model should inherit from this class. Also,
    """

    def __init__(self):
        pass

    @classmethod
    def first(cls):
        return session.query(cls).first()

    @classmethod
    def last(cls):
        return session.query(cls).last()

    @classmethod
    def all(cls):
        return session.query(cls).all()

    def delete(self):
        session.delete(self)
        session.commit()

    def save(self):
        session.add(self)
        session.commit()