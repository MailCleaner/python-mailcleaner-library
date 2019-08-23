#!/usr/bin/env python3
import logging

from mailcleaner.db.models import Fail2banJail
from mailcleaner.dumper.MailCleanerBaseDump import MailCleanerBaseDump


class DumpFail2banConfig(MailCleanerBaseDump):
    """
    Fail2ban Dumper - This dumper take care of dumping fail2ban jails.
    """
    def dump(self) -> None:
        """
        Dump Fail2Ban jails configuration files.
        :return None
        """
        self.dump_ssh_jail_conf()
        self.dump_exim_jail_conf()
        self.dump_webauth_jail_conf()

    def dump_ssh_jail_conf(self) -> None:
        """
        Dump SSH jail configuration.
        :return None
        """
        self.__dump_jail("mc-ssh")

    def dump_exim_jail_conf(self) -> None:
        """
        Dump SSH jail configuration.
        :return None
        """
        self.__dump_jail("mc-exim")

    def dump_webauth_jail_conf(self) -> None:
        """
        Dump SSH jail configuration.
        :return None
        """
        self.__dump_jail("mc-webauth")

    def __dump_jail(self, jail: str) -> None:
        """
        Dump SSH jail configuration.
        :return None
        """
        logging.info("Start dumping of {} jail conf ..".format(jail))

        mc_jail = Fail2banJail.find_by_name(name=jail.replace('-', '_'))
        if mc_jail is not None:
            self.dump_template(
                template_config_src_file='etc/fail2ban/jail.d/{}.local_template'
                .format(jail),
                config_datas=vars(mc_jail))
