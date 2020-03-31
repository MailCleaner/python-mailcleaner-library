#!/usr/bin/env python3

from mailcleaner.db import base
from sqlalchemy import Column, String, BLOB
from sqlalchemy.dialects.mysql import INTEGER
from . import BaseModel


class TrustedSources(base, BaseModel):
    """
    trustedSources table
    """
    __tablename__ = 'trustedSources'

    set_id = Column(INTEGER(11), nullable=False, primary_key=True, default=1)
    use_alltrusted = Column(INTEGER(1), nullable=False, default=1)
    use_authservers = Column(INTEGER(1), nullable=False, default=1)
    useSPFOnLocal = Column(INTEGER(1), nullable=False, default=1)
    useSPFOnGlobal = Column(INTEGER(1), nullable=False, default=0)
    authstring = Column(String(250), nullable=True)
    authservers = Column(BLOB, nullable=True)
    domainsToSPF = Column(BLOB, nullable=True)
    whiterbls = Column(BLOB, nullable=True)

