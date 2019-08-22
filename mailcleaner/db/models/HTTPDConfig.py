#!/usr/bin/env python3
from mailcleaner.db import base, session
from sqlalchemy import Column, String, BLOB, Boolean
from sqlalchemy.dialects.mysql import INTEGER
from . import BaseModel


class HTTPDConfig(base, BaseModel):
    """
    httpd_config table
    @TODO: - verify that every property fits correctly the table structure
    """
    __tablename__ = 'httpd_config'

    set_id = Column(INTEGER(1), primary_key=True, default=1)
    serveradmin = Column(String(150), nullable=False, default="")
    servername = Column(String(150), nullable=False, default="")
    use_ssl = Column(Boolean, nullable=False, default=True)
    timeout = Column(INTEGER(5), nullable=False, default=300)
    keepalivetimeout = Column(INTEGER(5), nullable=False, default=100)
    min_servers = Column(INTEGER(5), nullable=False, default=100)
    max_servers = Column(INTEGER(5), nullable=False, default=100)
    start_servers = Column(INTEGER(5), nullable=False, default=100)
    http_port = Column(INTEGER(3), nullable=False, default=80)
    https_port = Column(INTEGER(3), nullable=False, default=443)
    certificate_file = Column(String(50), nullable=False, default="default.pem")
    tls_certificate_data = Column(BLOB)
    tls_certificate_key = Column(BLOB)
    tls_certificate_chain = Column(BLOB)


