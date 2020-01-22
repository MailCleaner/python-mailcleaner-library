#!/usr/bin/env python3
from enum import Enum

from mailcleaner.config import MailCleanerConfig


class DBConfig(Enum):
    """
    Database Configuration
    """
    DB_USER = "mailcleaner"
    DB_NAME = "mc_config"
    DB_PASSWORD = MailCleanerConfig.get_instance().get_value(
        'MYMAILCLEANERPWD')
    IS_MASTER = MailCleanerConfig.get_instance().get_value('ISMASTER')
    DB_MASTER_IP = MailCleanerConfig.get_instance().get_value('MASTERIP')
    DB_MASTER_PWD = MailCleanerConfig.get_instance().get_value('MASTERPWD')
