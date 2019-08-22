#!/usr/bin/env python3
import logging
import os
import re

from invoke import run

from mailcleaner.db.models import SystemConf, MTAConfig
from mailcleaner.dumper.MailCleanerBaseDump import MailCleanerBaseDump
from mailcleaner.config import MailCleanerConfig

# Disable invoke library logging noise
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

    def get_qualify_domain(self) -> str:
        """
        Define the qualify domain used by MailCleaner. This value is defined by first looking at the default_domain
        configured by the administrator of MailCleaner. If nothing is configured then we will get this value by looking
        at the hostname.
        :return: the qualified domain of this MailCleaner host
        """
        qualify_domain = ""
        logging.debug("default_domain = ".format(self.system_conf.default_domain))
        if "^" not in self.system_conf.default_domain or "*" not in self.system_conf.default_domain:
            qualify_domain = self.system_conf.default_domain
        else:
            qualify_domain_result = run("/bin/hostname --fqdn", hide=True, warn=True)
            if qualify_domain_result.ok:
                qualify_domain = qualify_domain_result.stdout
                if qualify_domain == "":
                    qualify_domain = self._mc_config.get_value("DEFAULTDOMAIN")
            else:
                logging.error("An error occured in getting helo name: {}".format(qualify_domain_result.stderr))
                exit(255)
        logging.debug("Qualify domain: {}".format(qualify_domain))
        return qualify_domain

    def get_helo_name(self) -> str:
        """
        Determine the HELO_NAME used by Exim for SMTP session.
        The HELO_NAME can be set in different ways. First, we look if the MailCleaner Configuration file contains this
        parameter and consider it if it's exists. Otherwise, we will look at qualify_domain and finally getting the
        inet address via ifconfig.
        :return: the helo_name of this MailCleaner host
        """
        if self._mc_config.get_value("HELONAME") is not "":
            helo_name = self._mc_config.get_value("HELONAME")
        else:
            helo_name = self.get_qualify_domain()
            if "." not in helo_name:
                result = run("/sbin/ifconfig | /bin/grep 'inet addr' | /bin/grep -v '127.0.0.1'", hide=True, warn=True)
                if result.ok:
                    inet_adr_search = re.search('inet addr:([0-9.]+)', result.stdout, re.IGNORECASE)
                    if inet_adr_search:
                        helo_name = inet_adr_search.group(1)
                    logging.debug("Found helo name: {}".format(inet_adr_search))
                else:
                    logging.error("An error occured in getting helo name: {}".format(result.stderr))
                    exit(255)
        logging.debug("Helo name: {}".format(helo_name))

        return helo_name

    def dump_exim_stage_1(self) -> None:
        """
        Dump exim_stage1 configuration file.
        """
        pass

    def dump_exim_stage_2(self) -> None:
        """
        Dump exim_stage2 configuration file.
        """
        self.dump_template(template_config_src_file='etc/exim/exim_stage2.conf_template',
                           config_datas={
                               "VARDIR": self._mc_config.get_value("VARDIR"),
                               "SRCDIR": self._mc_config.get_value("SRCDIR"),
                               "helo_name": self.get_helo_name(),
                               "qualify_recipient": self.system_conf.sysadmin,
                               "usetls": self.exim_stage_2.use_incoming_tls,
                               "ignore_bounce_error_after": self.exim_stage_2.ignore_bounce_after,
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
