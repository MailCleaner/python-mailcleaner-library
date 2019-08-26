#!/usr/bin/env python3
import logging
import os
import re

from invoke import run

from mailcleaner.db.models import SystemConf, MTAConfig
from mailcleaner.dumper.MailCleanerBaseDump import MailCleanerBaseDump
from mailcleaner.config import MailCleanerConfig

# Disable invoke library logging noise
from mailcleaner.network import get_helo_name

logger = logging.getLogger("invoke")
logger.setLevel(logging.ERROR)


class DumpEximConfig(MailCleanerBaseDump):

    _mc_config = MailCleanerConfig.get_instance()
    exim_stage_1 = MTAConfig.find_by_set_id_and_stage_id(set_id=1, stage_id=1)
    exim_stage_2 = MTAConfig.find_by_set_id_and_stage_id(set_id=1, stage_id=2)
    exim_stage_4 = MTAConfig.find_by_set_id_and_stage_id(set_id=1, stage_id=4)
    system_conf = SystemConf.first()

    def dump(self) -> None:
        """
        Dump all exim stages configuration files.
        """
        self.dump_exim_stage_1()
        self.dump_exim_stage_2()
        self.dump_exim_stage_4()


    def dump_exim_stage_1(self) -> None:
        """
        Dump exim_stage1 configuration file.
        """
        pass

    def dump_exim_stage_2(self) -> None:
        """
        Dump exim_stage2 configuration file.
        """
        self.dump_template(
            template_config_src_file='etc/exim/exim_stage2.conf_template',
            config_datas={
                "VARDIR": self._mc_config.get_value("VARDIR"),
                "SRCDIR": self._mc_config.get_value("SRCDIR"),
                "helo_name": get_helo_name(),
                "qualify_recipient": self.system_conf.sysadmin,
                "usetls": self.exim_stage_2.use_incoming_tls,
                "ignore_bounce_error_after":
                self.exim_stage_2.ignore_bounce_after,
                "timeout_frozen_after": self.exim_stage_2.timeout_frozen_after,
                "global_maxmsgsize": self.exim_stage_2.global_msg_max_size,
                "max_received": self.exim_stage_2.received_headers_max,
                "received_header_text": self.exim_stage_2.header_txt,
            })

    def dump_exim_stage_4(self) -> None:
        """
        Dump exim_stage4 configuration file.
        """
        pass
