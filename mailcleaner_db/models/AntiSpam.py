import enum

from mailcleaner_db import base, session
from sqlalchemy import Column, String, BLOB, Boolean, Enum
from sqlalchemy.dialects.mysql import INTEGER
from mailcleaner_db.models.BaseModel import BaseModel


class AntiSpam(base, BaseModel):
    """
    antispam table
    @TODO: - verify that every property fits correctly the table structure
    """
    __tablename__ = 'antispam'

    set_id = Column(INTEGER(10), primary_key=True)
    use_spamassassin = Column(Boolean, nullable=False, default=True)
    spamassassin_timeout = Column(INTEGER(2), nullable=False, default=20)
    use_bayes = Column(Boolean, nullable=False, default=True)
    bayes_autolearn = Column(Boolean, nullable=False, default=False)
    ok_languages = Column(String(50), nullable=False, default="fr en de it es")
    ok_locales = Column(String(50), nullable=False, default="fr en de it es")
    use_rbls = Column(Boolean, nullable=False, default=True)
    rbls_timeout = Column(INTEGER(11), nullable=False, default=20)
    sa_rbls = Column(String(250), nullable=False, default="SORBS RFCIGNORANT DSBL AHBL SPAMCOP BSP IADB HABEAS DNSWL URIBL")
    use_dcc = Column(Boolean, nullable=False, default=True)
    dcc_timeout = Column(INTEGER(11), nullable=False, default=10)
    use_razor = Column(Boolean, nullable=False, default=True)
    razor_timeout = Column(INTEGER(11), nullable=False, default=10)
    use_pyzor = Column(Boolean, nullable=False, default=True)
    pyzor_timeout = Column(INTEGER(11), nullable=False, default=10)
    enable_whitelists = Column(Boolean, nullable=False, default=False)
    enable_warnlists = Column(Boolean, nullable=False, default=False)
    enable_blacklists = Column(Boolean, nullable=False, default=False)
    tag_mode_bypass_whitelist = Column(Boolean, nullable=False, default=True)
    trusted_ips = Column(BLOB)
    use_fuzzyocr = Column(Boolean, nullable=False, default=True)
    use_pdfinfo = Column(Boolean, nullable=False, default=True)
    use_imageinfo = Column(Boolean, nullable=False, default=True)
    use_botnet = Column(Boolean, nullable=False, default=True)
    use_domainkeys = Column(Boolean, nullable=False, default=True)
    domainkeys_timeout = Column(INTEGER(11), nullable=False, default=5)
    use_spf = Column(Boolean, nullable=False, default=True)
    spf_timeout = Column(INTEGER(11), nullable=False, default=5)
    use_dkim = Column(Boolean, nullable=False, default=True)
    dkim_timeout = Column(INTEGER(11), nullable=False, default=5)
    dmarc_follow_quarantine_policy = Column(Boolean, nullable=False, default=True)
    spam_list_to_be_spam = Column(INTEGER(11), nullable=False, default=2)
    use_syslog = Column(Boolean, nullable=False, default=False)
    do_stockme = Column(Boolean, nullable=False, default=False)
    stockme_nbdays = Column(INTEGER(11), nullable=False, default=3)
    dnsliststoreport = Column(String(50), nullable=False, default="")





