import os

from mailcleaner.dumper.MailCleanerBaseDump import MailCleanerBaseDump
from mailcleaner.config import MailCleanerConfig
from mailcleaner.db.models import Master


class DumpProxyConfig(MailCleanerBaseDump):

    _mc_config = MailCleanerConfig.get_instance()

    def dump(self) -> None:
        """
        Dump Mysql-Proxy configuration.
        :return: None
        """
        master = Master.first()
        self.dump_template(
            template_config_src_file='etc/mysql-proxy/proxy.cnf_template',
            config_datas={
                "username": 'mailcleaner',
                "password": self._mc_config.get_value("MYMAILCLEANERPWD"),
                "master_ip": master.hostname
            })
