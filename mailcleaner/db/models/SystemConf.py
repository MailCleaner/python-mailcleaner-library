#!/usr/bin/env python3
from mailcleaner.db import base
from sqlalchemy import Column, String, BLOB, Boolean
from sqlalchemy.dialects.mysql import INTEGER
from . import BaseModel
from sqlalchemy.dialects.mysql import TIME


class SystemConf(base, BaseModel):
    """
    antispam table
    @TODO: - verify that every property fits correctly the table structure
    """
    __tablename__ = 'system_conf'

    id = Column(INTEGER(10), primary_key=True)
    organisation = Column(String(200), nullable=False, default="")
    company_name = Column(String(200), nullable=False, default="")
    contact = Column(String(200), nullable=False, default="")
    contact_email = Column(String(200), nullable=False, default="")
    hostname = Column(String(200), nullable=False, default="")
    hostid = Column(INTEGER(11), nullable=False, default=1)
    clientid = Column(INTEGER(20), nullable=False)
    default_domain = Column(String(200), nullable=False, default="")
    default_language = Column(String(50), nullable=False, default="")
    sysadmin = Column(String(200), nullable=False, default="")
    days_to_keep_spams = Column(INTEGER(10), nullable=False, default=60)
    days_to_keep_virus = Column(INTEGER(10), nullable=False, default=60)
    cron_time = Column(TIME, nullable=False, default="00:00:00")
    cron_weekday = Column(INTEGER(2), nullable=False, default=1)
    cron_monthday = Column(INTEGER(2), nullable=False, default=1)
    summary_subject = Column(String(250),
                             nullable=False,
                             default="Mailcleaner quarantine summary")
    summary_from = Column(String(200),
                          nullable=False,
                          default="your_mail@yourdomain")
    analyse_to = Column(String(200),
                        nullable=False,
                        default="your_mail@yourdomain")
    falseneg_to = Column(String(200),
                         nullable=False,
                         default="your_mail@yourdomain")
    falsepos_to = Column(String(200),
                         nullable=False,
                         default="your_mail@yourdomain")
    src_dir = Column(String(255), nullable=False, default="/opt/mailcleaner")
    var_dir = Column(String(255), nullable=False, default="/var/mailcleaner")
    ad_server = Column(String(80), nullable=False, default="")
    ad_param = Column(String(200), nullable=False, default="")
    http_proxy = Column(String(200), nullable=False, default="")
    use_syslog = Column(Boolean, nullable=False, default=False)
    syslog_host = Column(String(200), nullable=False, default="")
    smtp_proxy = Column(String(200), nullable=False, default="")
    use_archiver = Column(Boolean, nullable=False, default=False)
    archiver_host = Column(String(200), nullable=False, default="")
    api_fulladmin_ips = Column(BLOB)
    api_admin_ips = Column(BLOB)
