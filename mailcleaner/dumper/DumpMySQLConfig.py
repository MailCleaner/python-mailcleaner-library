#!/usr/bin/env python3
import os

from mailcleaner.dumper.MailCleanerBaseDump import MailCleanerBaseDump
from mailcleaner.config import MailCleanerConfig


class DumpMySQLConfig(MailCleanerBaseDump):
    """
    MySQL Dumper - Take care of dumping MySQL configuration files.
    """

    _mc_config = MailCleanerConfig.get_instance()
    binary_log_keep = 0

    def dump(self) -> None:
        """
        Dump MySQL configuration (master and slave).
        :return: None
        """
        # Avoid having unsychronized database when starting a new VA
        if os.path.exists(
                self._mc_config.get_value("VARDIR") +
                "/run/configurator/updater4mc-ran"):
            self.binary_log_keep = 21

        self.dump_master_config()
        self.dump_slave_config()

    def dump_master_config(self) -> None:
        """
        Dump MySQL master configuration.
        :return: None
        """
        MASTERID = (int(self._mc_config.get_value("HOSTID")) * 2) - 1 + 10
        self.dump_template(
            template_config_src_file='etc/mysql/my_master.cnf_template',
            config_datas={
                "VARDIR": self._mc_config.get_value("VARDIR"),
                "MASTERID": MASTERID,
                "binary_log_keep": self.binary_log_keep
            })

    def dump_slave_config(self) -> None:
        """
        Dump MySQL slave configuration.
        :return: None
        """
        SLAVEID = int(self._mc_config.get_value("HOSTID")) * 2 + 10
        self.dump_template(
            template_config_src_file='etc/mysql/my_slave.cnf_template',
            config_datas={
                "VARDIR": self._mc_config.get_value("VARDIR"),
                "slave_id": SLAVEID,
                "binary_log_keep": self.binary_log_keep
            })
