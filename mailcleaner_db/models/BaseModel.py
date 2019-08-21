from mailcleaner_db import base, session


class AutoRepr(object):
    """
    Generate the __repr__ function for every class inheriting from. Used for Models.
    """
    def __repr__(self):
        items = ("%s = %r" % (k, v) for k, v in self.__dict__.items())
        return "<%s: {%s}>" % (self.__class__.__name__, ', '.join(items)) + "\n"


class BaseModel(AutoRepr):
    """
    Base Model for creating a MailCleaner Model related to a table of mc_config db.
    Every model should inherit from this class. Also, common functions of Models should be placed here.
    """

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
