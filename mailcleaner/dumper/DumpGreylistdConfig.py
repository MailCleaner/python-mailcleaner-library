#!/usr/bin/env python3
import os

from mailcleaner.dumper.MailCleanerBaseDump import MailCleanerBaseDump
from mailcleaner.config import MailCleanerConfig
from mailcleaner.db.models import GreylistdConfig


class DumpGreylistdConfig(MailCleanerBaseDump):

    _mc_config = MailCleanerConfig.get_instance()
    _greylistd_config = GreylistdConfig().first()

    def dump(self) -> None:
        """
        Dump Greylistd configuration.
        :return: None
        """

        self.dump_template(
            template_config_src_file='etc/greylistd/greylistd.conf_template',
            config_datas={
                "VARDIR": self._mc_config.get_value("VARDIR"),
                "retry_min": self._greylistd_config.retry_min,
                "retry_max": self._greylistd_config.retry_max,
                "expire": self._greylistd_config.expire,
            })

    def dump_domains_to_avoid(self) -> None:
        self.write_to_file(
            self._greylistd_config.avoid_domains.decode('utf-8').split('\r\n'),
            "{}/spool/tmp/mailcleaner/domains_to_avoid_greylist.list".format(
                self._mc_config.get_value("VARDIR")))