from mailcleaner_db import base, session
from sqlalchemy import Column, Integer, String, Boolean

from mailcleaner_db.models.BaseModel import BaseModel


class Fail2banJail(base, BaseModel):

    """
    Fail2banJail table
    """
    __tablename__ = 'fail2ban_jail'

    id = Column(Integer, primary_key=True)
    enabled = Column(Boolean, nullable=True, default=True)
    name = Column(String(150), nullable=False, unique=True)
    maxretry = Column(Integer, nullable=False)
    findtime = Column(Integer, nullable=False)
    bantime = Column(Integer, nullable=False)
    port = Column(String(50), nullable=False)
    filter = Column(String(50), nullable=False)
    banaction = Column(String(50), nullable=False)
    logpath = Column(String(250), nullable=False)

    def __repr__(self):
        return "<Fail2banJail id={} enabled={} name={} " \
               "maxretry={} findtime={} bantime={} port={} filter={} banaction={} logpath={}>\n"\
                .format(self.id, self.enabled, self.name, self.maxretry, self.findtime, self.bantime, self.port,
                       self.filter, self.banaction, self.logpath)

    @classmethod
    def find_by_id(cls, id: int):
        return session.query(Fail2banJail).filter_by(id=id).first()

    @classmethod
    def find_by_name(cls, name: str):
        return session.query(Fail2banJail).filter_by(name=name).first()
