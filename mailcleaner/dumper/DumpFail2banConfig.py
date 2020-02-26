#!/usr/bin/env python3
import logging

from mailcleaner.db.models import Fail2banJail
from mailcleaner.db.models import Fail2banIps
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

    def dump_all_from_mysql(self) -> None:
        """
        Dump all jails in DB
        """
        jails = Fail2banJail().get_jails()
        for jail in jails:
            self.__dump_jail(jail[0])

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
        mc_jail = Fail2banJail.find_by_name(name=jail)
        raw_whitelisted_ip = Fail2banIps.find_by_whitelisted_and_jail(jail)
        list_whitelisted = []
        for whitelisted_ip in raw_whitelisted_ip:
            list_whitelisted.append(whitelisted_ip.ip)
        varrr = {
            'name': mc_jail.name,
            'enabled': mc_jail.enabled,
            'maxretry': mc_jail.maxretry,
            'findtime': mc_jail.findtime,
            'bantime': mc_jail.bantime,
            'port': mc_jail.port,
            'filter': mc_jail.filter,
            'whitelist': list_whitelisted,
            'banaction': mc_jail.banaction,
            'logpath': mc_jail.logpath,
        }
        if mc_jail is not None:
            self.dump_template(
                template_config_src_file=
                'etc/fail2ban/jail.d/default.local_template',
                destination_config_src_file='etc/fail2ban/jail.d/{}.local'.
                format(jail),
                config_datas=varrr)
            self.dump_template(
                template_config_src_file=
                'etc/fail2ban/jail.d/default-bl.local_template',
                destination_config_src_file='etc/fail2ban/jail.d/{}-bl.local'.
                format(jail),
                config_datas={
                    "name": mc_jail.name + "-bl",
                    "enabled": mc_jail.enabled,
                    "port": mc_jail.port
                })
