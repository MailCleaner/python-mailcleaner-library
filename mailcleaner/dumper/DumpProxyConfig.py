from mailcleaner.dumper.MailCleanerBaseDump import MailCleanerBaseDump
from mailcleaner.config import MailCleanerConfig
from mailcleaner.db.models import Master
from mailcleaner.db.models import Slave


class DumpProxyConfig(MailCleanerBaseDump):

    _mc_config = MailCleanerConfig.get_instance()

    def dump(self) -> None:
        """
        Dump Proxy-Sql configuration.
        :return: None
        """
        master = Master.first()
        slaves_list = []
        slaves_hosts = Slave.get_all_slaves()
        for slave_host in slaves_hosts:
            slave_list = {}
            slave_list["hostname"] = slave_host.hostname
            slave_list["port"] = slave_host.port
            slaves_list.append(slave_list)
        
        self.dump_template(
            template_config_src_file='etc/proxysql/proxysql.conf_template',
            config_datas={
                "username": 'mailcleaner',
                "password": self._mc_config.get_value("MYMAILCLEANERPWD"),
                "VARDIR": self._mc_config.get_value("VARDIR"),
                "master_host": {"hostname" : master.hostname, "port": master.port},
                "slaves_hosts": slaves_list
            })