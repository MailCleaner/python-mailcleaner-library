#!/usr/bin/env python3

from sqlalchemy import Column, String, Boolean
from sqlalchemy.dialects.mysql import INTEGER

from mailcleaner.db import base
from . import BaseModel


class UserPref(base, BaseModel):
    """
    user_pref table
    """
    __tablename__ = 'user_pref'

    id = Column(INTEGER(11), nullable=False, primary_key=True)
    viruswall = Column(Boolean, nullable=False, default=True)
    spamwall = Column(Boolean, nullable=False, default=True)
    block_bad_tnef = Column(Boolean, nullable=False, default=False)
    block_encrypted = Column(Boolean, nullable=False, default=False)
    block_unencrypted = Column(Boolean, nullable=False, default=False)
    allow_passprotected_archives = Column(Boolean, nullable=False, default=False)
    allow_partial = Column(Boolean, nullable=False, default=False)
    allow_external_bodies = Column(Boolean, nullable=False, default=False)
    allow_iframe = Column(Boolean, nullable=False, default=False)
    allow_forms = Column(Boolean, nullable=False, default=True)
    allow_scripts = Column(Boolean, nullable=False, default=False)
    allow_codebase = Column(Boolean, nullable=False, default=False)
    convert_danger_to_text = Column(Boolean, nullable=False, default=False)
    convert_html_to_text = Column(Boolean, nullable=False, default=False)
    notify_sender = Column(Boolean, nullable=False, default=True)
    notify_virus_sender = Column(Boolean, nullable=False, default=False)
    notify_blocked_sender = Column(Boolean, nullable=False, default=True)
    notify_blocked_content = Column(Boolean, nullable=False, default=True)
    virus_modify_subject = Column(Boolean, nullable=False, default=True)
    virus_subject = Column(String(20), nullable=False, default="{Virus?}")
    file_modify_subject = Column(Boolean, nullable=False, default=True)
    file_subject = Column(String(20), nullable=False, default="{Virus?}")
    content_modify_subject = Column(Boolean, nullable=False, default=True)
    content_subject = Column(String(20), nullable=False, default="{Virus?}")
    warning_attach = Column(Boolean, nullable=False, default=True)
    warning_filename = Column(String(50), nullable=False, default="AttentionVirus.txt")
    warning_encoding_charset = Column(String(20), nullable=False, default="ISO-8859-1")
    use_bayes = Column(Boolean, nullable=False, default=True)
    ok_languages = Column(String(50), nullable=False, default="fr en de it es")
    ok_locales = Column(String(50), nullable=False, default="fr en de it es")
    use_rbls = Column(Boolean, nullable=False, default=True)
    use_dcc = Column(Boolean, nullable=False, default=True)
    use_razor = Column(Boolean, nullable=False, default=True)
    use_pyzor = Column(Boolean, nullable=False, default=True)
    delivery_type = Column(INTEGER(11), nullable=False, default=True)
    daily_summary = Column(Boolean, nullable=False, default=False)
    weekly_summary = Column(Boolean, nullable=False, default=True)
    monthly_summary = Column(Boolean, nullable=False, default=False)
    summary = Column(Boolean, nullable=False, default=True)
    summary_freq = Column(INTEGER(11), nullable=False, default=True)
    summary_type = Column(String(20), nullable=False, default="NOTSET")
    summary_to = Column(String(200), nullable=True, default="NULL")
    spam_tag = Column(String(20), nullable=False, default="{Spam?}")
    quarantine_bounces = Column(Boolean, nullable=False, default=False)
    has_whitelist = Column(Boolean, nullable=False, default=False)
    has_warnlist = Column(Boolean, nullable=False, default=False)
    has_blacklist = Column(Boolean, nullable=False, default=False)
    language = Column(String(10), nullable=False)
    gui_displayed_spams = Column(INTEGER(11), nullable=False, default=20)
    gui_displayed_days = Column(INTEGER(11), nullable=False, default=7)
    gui_mask_forced = Column(Boolean, nullable=False, default=False)
    gui_default_address = Column(String(200), nullable=True)
    gui_graph_type = Column(String(20), nullable=False, default="bar")
    gui_group_quarantines = Column(Boolean, nullable=True)
    archive_mail = Column(Boolean, nullable=False, default=False)
    archive_spam = Column(Boolean, nullable=False, default=False)
    copyto_mail = Column(String(250), nullable=True)
    bypass_filtering = Column(Boolean, nullable=False, default=False)
    allow_newsletters = Column(Boolean, nullable=False, default=True)
