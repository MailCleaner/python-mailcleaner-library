import os

from mailcleaner.config import MailCleanerConfig


def has_updater_ran() -> bool:
    """
    Verify if the Updater4MC has been ran.
    :return: True if updater4mc-ran file exists, False otherwise
    """
    mailcleaner_config = MailCleanerConfig.get_instance()
    return os.path.exists(
        mailcleaner_config.get_value("VARDIR") +
        "/run/configurator/updater4mc-ran")
