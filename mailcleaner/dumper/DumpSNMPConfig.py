#!/usr/bin/env python3
import os

from mailcleaner.dumper.MailCleanerBaseDump import MailCleanerBaseDump
from mailcleaner.config import MailCleanerConfig
from mailcleaner.db.models import SNMPDConfig


class DumpSNMPConfig(MailCleanerBaseDump):
    """
    SNMP Dumper - Take care of dumping SNMP configuration files.
    """
    _mc_config = MailCleanerConfig.get_instance()

    def dump(self) -> None:
        """
        Dump SNMP configuration.
        :return: None
        """
        snmpd_config = SNMPDConfig().first()
        self.dump_template(
            template_config_src_file='etc/snmp/snmpd.conf_template',
            config_datas={
                "SRCDIR": self._mc_config.get_value("SRCDIR"),
                "ips": snmpd_config.allowed_ip.split("\r\n"),
                "community": snmpd_config.community,
                "disks": snmpd_config.disks.split(":"),
            })