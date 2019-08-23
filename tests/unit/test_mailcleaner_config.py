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


def test_change_config_with_existing_key():
    mailcleaner_configuration = MailCleanerConfig()
    host_id = mailcleaner_configuration.get_value("HOSTID")
    result_change = mailcleaner_configuration.change_configuration("HOSTID", "42")
    assert host_id is not None
    assert host_id is not ""
    assert result_change
    assert mailcleaner_configuration.get_value("HOSTID") == "42"
    assert mailcleaner_configuration.change_configuration("HOSTID", host_id)

def test_change_config_with_unknown_key():
    mailcleaner_configuration = MailCleanerConfig()
    unkown_key = mailcleaner_configuration.get_value("UNKOWNKEY")
    result_change = mailcleaner_configuration.change_configuration("UNKOWNKEY", "42")
    assert unkown_key is ""
    assert not result_change
