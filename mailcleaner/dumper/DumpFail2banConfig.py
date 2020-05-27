#!/usr/bin/env python3
import logging

from mailcleaner.db.models import Fail2banJail
from mailcleaner.db.models import Fail2banIps
from mailcleaner.db.models.Fail2banConfig import Fail2banConfig
from mailcleaner.db.models.Registration import Registration
from mailcleaner.dumper.MailCleanerBaseDump import MailCleanerBaseDump
from mailcleaner.config import MailCleanerConfig


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

    def dump_jail(self, jail: str) -> None:
        mc_jail = Fail2banJail.find_by_name(name=jail)
        if mc_jail != None:
            self.__dump_jail(jail)

    def dump_sendmail_common(self):
        logging.info("Start dumping of sendmail-common conf ..")
        gen_conf = Fail2banConfig().first()
        self.dump_template(
            template_config_src_file=
            'etc/fail2ban/action.d/sendmail-common.conf_template',
            destination_config_src_file=
            'etc/fail2ban/action.d/sendmail-common.conf',
            config_datas={
                'src_name': gen_conf.src_name,
                'src_email': gen_conf.src_email,
                'dest_email': gen_conf.dest_email,
            })

    def check_rbl_send(self) -> bool:
        if MailCleanerConfig.get_instance().get_value("REGISTERED") == "1":
            return True
        elif MailCleanerConfig.get_instance().get_value("REGISTERED") == "2":
            reg = Registration().first()
            if reg.accept_send_statistics:
                return True
            else:
                return False
        else:
            return False

    def __dump_jail(self, jail: str) -> None:
        """
        Dump SSH jail configuration.
        :return None
        """
        logging.info("Start dumping of {} jail conf ..".format(jail))
        mc_jail = Fail2banJail.find_by_name(name=jail)
        if mc_jail is not None:
            #-- Jail Dump --#
            raw_whitelisted_ip = Fail2banIps.find_by_whitelisted_and_jail(jail)
            list_whitelisted = []
            for whitelisted_ip in raw_whitelisted_ip:
                list_whitelisted.append(whitelisted_ip.ip)
            send_mail = ""
            if mc_jail.send_mail != False:
                send_mail = "sendmail"
            send_rbl = ""
            enabled = mc_jail.enabled
            banaction = mc_jail.banaction
            if self.check_rbl_send():
                if enabled:
                    send_rbl = "mc-send-rbl"
                else:
                    enabled = True
                    banaction = "mc-send-rbl"
            varrr = {
                'name': mc_jail.name,
                'enabled': enabled,
                'maxretry': mc_jail.maxretry,
                'findtime': mc_jail.findtime,
                'bantime': mc_jail.bantime,
                'port': mc_jail.port,
                'filter': mc_jail.filter,
                'whitelist': list_whitelisted,
                'banaction': banaction,
                'logpath': mc_jail.logpath,
                "send_rbl": send_rbl,
                'send_mail': send_mail
            }
            self.dump_template(
                template_config_src_file=
                'etc/fail2ban/jail.d/default.local_template',
                destination_config_src_file='etc/fail2ban/jail.d/{}.local'.
                format(jail),
                config_datas=varrr)
            #-- Blacklist Dump --#
            enabled = False
            send_mail_bl = ""
            if mc_jail.send_mail_bl != False:
                send_mail_bl = "sendmail"
            if mc_jail.max_count != -1:
                enabled = True
            self.dump_template(
                template_config_src_file=
                'etc/fail2ban/jail.d/default-bl.local_template',
                destination_config_src_file='etc/fail2ban/jail.d/{}-bl.local'.
                format(jail),
                config_datas={
                    "name": mc_jail.name + "-bl",
                    "enabled": enabled,
                    "port": mc_jail.port,
                    "send_mail": send_mail_bl,
                })
