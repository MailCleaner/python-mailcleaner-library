from mailcleaner_db import base, session
from sqlalchemy import Column, Integer, String, Boolean

from mailcleaner_db.models.BaseModel import BaseModel


class Fail2banIps(base, BaseModel):

    """
    Fail2banIps table
    """
    __tablename__ = 'fail2ban_ips'

    id = Column(Integer, primary_key=True)
    ip = Column(String(150), nullable=False)
    count = Column(Integer, nullable=False)
    active = Column(Boolean, nullable=True, default=True)
    blacklisted = Column(Boolean, nullable=True, default=False)
    whitelisted = Column(Boolean, nullable=True, default=False)
    jail = Column(String(20), nullable=False)

    @classmethod
    def find_by_id(cls, id: int):
        return session.query(Fail2banIps).filter_by(id=id).first()

    @classmethod
    def find_by_ip(cls, ip: str):
        return session.query(Fail2banIps).filter_by(ip=ip).all()

    @classmethod
    def find_by_active(cls, active: bool = True):
        return session.query(Fail2banIps).filter_by(active=active).all()

    @classmethod
    def find_by_jail(cls, domain: str):
        return session.query(Fail2banIps).filter_by(domain=domain).all()

    @classmethod
    def find_by_ip_and_jail(cls, ip: str, jail: str):
        return session.query(Fail2banIps).filter(ip == ip, jail == jail).first()

    @classmethod
    def find_by_blacklisted_and_ip_and_jail(cls, blacklisted: bool, ip: str, jail: str):
        return session.query(Fail2banIps).filter(blacklisted == blacklisted, ip == ip, jail == jail).first()

    @classmethod
    def find_by_whitelisted_and_ip_and_jail(cls, whitelisted: bool, ip: str, jail: str):
        return session.query(Fail2banIps).filter(whitelisted == whitelisted, ip == ip, jail == jail).first()

