#!/usr/bin/env python3
from mailcleaner.db import base, session
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP
from sqlalchemy.sql import func
import factory
from . import BaseModel


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
    last_hit = Column(TIMESTAMP, server_default=func.now())
    host = Column(String(150), nullable=False)

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
    def find_by_host(cls, host: str):
        return session.query(Fail2banIps).filter_by(host=host).all()

    @classmethod
    def find_by_ip_and_jail(cls, ip: str, jail: str):
        return session.query(Fail2banIps).filter(
            Fail2banIps.ip == ip, Fail2banIps.jail == jail).first()

    @classmethod
    def find_by_whitelisted_and_jail(cls, jail: str, whitelisted: bool = True):
        return session.query(Fail2banIps).filter(
            Fail2banIps.whitelisted == whitelisted, Fail2banIps.jail == jail).all()

    @classmethod
    def find_by_blacklisted_and_jail(cls, jail: str, blacklisted: bool = True):
        return session.query(Fail2banIps).filter(
            Fail2banIps.blacklisted == blacklisted, Fail2banIps.jail == jail).all()

    @classmethod
    def find_by_blacklisted_and_ip_and_jail(cls, blacklisted: bool, ip: str,
                                            jail: str):
        return session.query(Fail2banIps).filter(
            Fail2banIps.blacklisted == blacklisted, Fail2banIps.ip == ip,
            Fail2banIps.jail == jail).first()

    @classmethod
    def find_by_whitelisted_and_ip_and_jail(cls, whitelisted: bool, ip: str,
                                            jail: str):
        return session.query(Fail2banIps).filter(
            Fail2banIps.whitelisted == whitelisted, Fail2banIps.ip == ip,
            Fail2banIps.jail == jail).first()

    @classmethod
    def get_all_active_by_jail(cls, jail:str, active:bool = True):
        return session.query(Fail2banIps).filter(
            Fail2banIps.active==active,
            Fail2banIps.jail==jail).all()
    @classmethod
    def set_all_active(cls, active:bool = False):
        actives = session.query(Fail2banIps).filter_by(active=active).all()
        for active in actives:
            active.active = active
        session.flush()
        session.commit()


class Fail2banIpsFactory(factory.alchemy.SQLAlchemyModelFactory):
    id = factory.Sequence(lambda n: n)
    ip = factory.Sequence(lambda n: n)
    count = 1
    active = 1
    blacklisted = 0
    whitelisted = 0
    jail = ""
    last_hit = func.now()
    host = ""
    class Meta:
        model = Fail2banIps
        sqlalchemy_session = session
