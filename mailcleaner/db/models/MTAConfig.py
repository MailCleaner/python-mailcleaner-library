#!/usr/bin/env python3
import enum

from mailcleaner.db import base, session
from sqlalchemy import Column, String, BLOB, Boolean, Enum
from sqlalchemy.dialects.mysql import INTEGER
from . import BaseModel


class MTAConfigBooleanEnum(enum.Enum):
    """
    MailCleaner MySQL Enum used for MTAConfig table
    """
    true = "true"
    false = "false"


class MTAConfig(base, BaseModel):
    """
    mta_config table
    @TODO: - verify that every property fits correctly the table structure
    """
    __tablename__ = 'mta_config'

    set_id = Column(INTEGER(10), primary_key=True)
    stage = Column(INTEGER(2), primary_key=True)
    header_txt = Column(BLOB, nullable=False)
    accept_8bitmime = Column(Enum(MTAConfigBooleanEnum), nullable=False)
    print_topbitchars = Column(Enum(MTAConfigBooleanEnum), nullable=False)
    return_path_remove = Column(Enum(MTAConfigBooleanEnum), nullable=False)
    ignore_bounce_after = Column(String(10), nullable=False, default="2d")
    timeout_frozen_after = Column(String(10), nullable=False, default="7d")
    smtp_relay = Column(Enum(MTAConfigBooleanEnum), nullable=False)
    relay_from_hosts = Column(BLOB)
    allow_relay_for_unknown_domains = Column(Boolean,
                                             nullable=True,
                                             default=False)
    no_ratelimit_hosts = Column(BLOB)
    smtp_enforce_sync = Column(Enum(MTAConfigBooleanEnum), nullable=False)
    allow_mx_to_ip = Column(Enum(MTAConfigBooleanEnum), nullable=False)
    smtp_receive_timeout = Column(String(10), nullable=False, default="30s")
    smtp_accept_max_per_host = Column(INTEGER(10), nullable=False, default=10)
    smtp_accept_max_per_trusted_host = Column(INTEGER(10),
                                              nullable=False,
                                              default=20)
    smtp_accept_max = Column(INTEGER(10), nullable=False, default=50)
    smtp_reserve = Column(INTEGER(10), nullable=False, default=5)
    smtp_load_reserve = Column(INTEGER(10), nullable=False, default=30)
    smtp_accept_queue_per_connection = Column(INTEGER(10),
                                              nullable=False,
                                              default=10)
    smtp_accept_max_per_connection = Column(INTEGER(10),
                                            nullable=False,
                                            default=100)
    smtp_conn_access = Column(String(10000), nullable=False, default="*")
    host_reject = Column(BLOB)
    sender_reject = Column(BLOB)
    recipient_reject = Column(BLOB)
    user_reject = Column(BLOB)
    verify_sender = Column(Boolean, nullable=True, default=True)
    global_msg_max_size = Column(String(50), nullable=False, default="50M")
    max_rcpt = Column(INTEGER(10), nullable=False, default=1000)
    received_headers_max = Column(INTEGER(10), nullable=False, default=30)
    use_incoming_tls = Column(Boolean, nullable=True, default=False)
    tls_certificate = Column(String(50), nullable=False, default="default")
    tls_use_ssmtp_port = Column(Boolean, nullable=True, default=False)
    tls_certificate_data = Column(BLOB)
    tls_certificate_key = Column(BLOB)
    hosts_require_tls = Column(BLOB)
    domains_require_tls_from = Column(BLOB)
    domains_require_tls_to = Column(BLOB)
    hosts_require_incoming_tls = Column(BLOB)
    use_syslog = Column(Boolean, nullable=True, default=False)
    smtp_banner = Column(
        String(255),
        nullable=False,
        default="$smtp_active_hostname ESMTP Exim $version_number $tod_full")
    errors_reply_to = Column(String(255), default="")
    rbls = Column(String(255))
    rbls_timeout = Column(INTEGER(10), default=5)
    rbls_ignore_hosts = Column(BLOB)
    bs_rbls = Column(String(255))
    rbls_after_rcpt = Column(Boolean, nullable=True, default=True)
    callout_timeout = Column(INTEGER(10), default=10)
    retry_rule = Column(String(255), nullable=False, default="F,4d,2m")
    ratelimit_enable = Column(Boolean, nullable=True, default=False)
    ratelimit_rule = Column(String(255),
                            nullable=False,
                            default="30 / 1m / strict")
    ratelimit_delay = Column(INTEGER(10), default=10)
    trusted_ratelimit_enable = Column(Boolean, nullable=True, default=False)
    trusted_ratelimit_rule = Column(String(255),
                                    nullable=False,
                                    default="60 / 1m / strict")
    trusted_ratelimit_delay = Column(INTEGER(10), default=10)
    outgoing_virus_scan = Column(Boolean, nullable=True, default=False)
    mask_relayed_ip = Column(Boolean, nullable=True, default=False)
    masquerade_outgoing_helo = Column(Boolean, nullable=True, default=False)
    forbid_clear_auth = Column(Boolean, nullable=True, default=False)
    relay_refused_to_domains = Column(BLOB)
    dkim_default_domain = Column(String(255))
    dkim_default_selector = Column(String(255))
    dkim_default_pkey = Column(BLOB)
    reject_bad_spf = Column(Boolean, nullable=True, default=False)
    reject_bad_rdns = Column(Boolean, nullable=True, default=False)
    dmarc_follow_reject_policy = Column(Boolean, nullable=True, default=False)
    dmarc_enable_reports = Column(Boolean, nullable=True, default=False)
    spf_dmarc_ignore_hosts = Column(BLOB)

    @classmethod
    def find_by_set_id_and_stage_id(cls, set_id: int, stage_id: int):
        return session.query(MTAConfig).filter(set_id == set_id,
                                               stage_id == stage_id).first()
