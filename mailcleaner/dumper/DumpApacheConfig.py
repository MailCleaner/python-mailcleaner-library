#!/usr/bin/env python3
import os

from mailcleaner.dumper.MailCleanerBaseDump import MailCleanerBaseDump
from mailcleaner.config import MailCleanerConfig
from mailcleaner.db.models import HTTPDConfig, SystemConf


class DumpApacheConfig(MailCleanerBaseDump):

    _httpd_config = HTTPDConfig.first()
    _mc_config = MailCleanerConfig.get_instance()
    _system_conf = SystemConf.first()

    def dump(self):
        """
        Dump Apache configuration.
        :return: None
        """
        self.dump_certs()
        self.dump_httpd()

    def dump_httpd(self):
        self.dump_template(
            template_config_src_file='etc/apache/httpd.conf_template',
            config_datas={
                "VARDIR": self._mc_config.get_value("VARDIR"),
                "SRCDIR": self._mc_config.get_value("SRCDIR"),
                "keep_alive_timeout": self._httpd_config.keepalivetimeout,
                "max_servers": self._httpd_config.max_servers,
                "min_servers": self._httpd_config.min_servers,
                "server_admin": self._httpd_config.serveradmin,
                "server_name": self._httpd_config.servername,
                "start_servers": self._httpd_config.start_servers,
                "timeout": self._httpd_config.timeout,
            })

    def dump_mailcleaner_site(self):
        self.dump_template(template_config_src_file=
                           'etc/apache/sites/mailcleaner.conf_template',
                           config_datas={
                               "VARDIR": self._mc_config.get_value("VARDIR"),
                               "SRCDIR": self._mc_config.get_value("SRCDIR"),
                               "http_port": self._httpd_config.http_port,
                               "https_port": self._httpd_config.https_port,
                               "server_name": self._httpd_config.servername,
                               "ssl_enabled": self._httpd_config.use_ssl,
                           })

    def dump_configurator_site(self):
        VARDIR = self._mc_config.get_value("VARDIR")
        if os.path.isfile(
                "{}/run/configurator/dis_conf_interface.enable".format(
                    VARDIR)):
            enabled = True
        else:
            enabled = False

        self.dump_template(template_config_src_file=
                           'etc/apache/sites/configurator.conf_template',
                           config_datas={
                               "VARDIR": VARDIR,
                               "SRCDIR": self._mc_config.get_value("SRCDIR"),
                               "enabled": enabled,
                           })

    def dump_soap_wsdl(self):
        self.dump_template(template_config_src_file=
                           'www/soap/htdocs/mailcleaner.wsdl_template',
                           config_datas={
                               "host": _system_conf.hostname,
                           })

    def dump_certs(self):
        # TODO : add it
        print()