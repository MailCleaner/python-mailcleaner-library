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
