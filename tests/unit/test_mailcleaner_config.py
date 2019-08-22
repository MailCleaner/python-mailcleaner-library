import os

from mailcleaner.config import MailCleanerConfig


def test_get_is_master():
    mailcleaner_configuration = MailCleanerConfig()
    assert mailcleaner_configuration.get_value('ISMASTER') in ['Y', 'N']


def test_get_and_check_dirs():
    mailcleaner_configuration = MailCleanerConfig()
    src_dir = mailcleaner_configuration.get_value('SRCDIR')
    var_dir = mailcleaner_configuration.get_value('VARDIR')
    assert src_dir == "/usr/mailcleaner"
    assert var_dir == "/var/mailcleaner"


def test_check_if_mc_config_file_exists():
    assert os.path.isfile('/etc/mailcleaner.conf')