#!/usr/bin/python
import subprocess, sys, os
import logging
import requests
try:
    from mailcleaner.config import MailCleanerConfig
    from .fail2ban_db import Fail2banDB
    from .fail2ban_db import Fail2banAction
    from .fail2ban_db import InsertError
    from mailcleaner.logger import McLogger
    from mailcleaner.db.models.Fail2banJail import Fail2banJail
    from mailcleaner.db.models.Fail2banIps import Fail2banIps
    from mailcleaner.dumper.DumpFail2banConfig import DumpFail2banConfig
except Exception as err:
    log_file = "/var/mailcleaner/log/mc_fail2ban_script.log"
    logging.basicConfig(
        filename=log_file,
        filemode='a+',
        format='%(asctime)s - [McFail2ban] - %(levelname)s - %(message)s',
        datefmt='%d-%b-%y %H:%M:%S',
        level=10)
    logging.warn("Cannot import package mailcleaner => {}".format(err))
    quit()
from invoke import run

dump_file_path = "/var/tmp/"


class Fail2banException(Exception):
    msg = ''

    def __init__(self, msg):
        super(Fail2banException, self).__init__(msg)


class Fail2banService:

    jail_name = ''
    ip = ''
    ip_type = 'IPV4'
    fail2banDB = None
    __mcLogger = None

    def __init__(self, jail_name: str = '', ip: str = ''):
        self.jail_name = jail_name
        self.ip = ip
        self.fail2banDB = Fail2banDB()
        self.__mcLogger = McLogger(name="Fail2banService",
                                   project="fail2ban",
                                   filename="mc-fail2ban")

    def set_ip(self, ip: str):
        self.ip = ip

    def __str__(self) -> str:
        return "jail: {0} ip:{1}".format(self.jail_name, self.ip)

    def set_jail_name(self, jail_name: str) -> None:
        self.jail_name = jail_name

    def ban(self,
            ip: str = None,
            jail_name: str = None,
            db_insert: bool = True,
            f2b_call: bool = False) -> None:
        """ 
            Ban an IP.
            Blacklist the IP, if it needs to
        Arguments:
            ip {str} -- ip address
            jail_name {str} -- Jail name
            db_insert {bool} -- Needs to insert to DB,
            f2b_call {bool} -- Needs to call F2B):
        """
        if ip == None:
            ip = self.ip
        if jail_name == None:
            jail_name = self.jail_name

        if f2b_call and self.__safe_run(
                "fail2ban-client status {0} |grep {1}".format(jail_name, ip),
                False,
                hide=True).return_code:
            self.__safe_run("fail2ban-client set {0} banip {1}".format(
                jail_name, ip))
        else:
            print("{0} is already banned in {1}".format(ip, jail_name))
        self.__mcLogger.info("Banning=>{0} inside jail=>{1}".format(
            ip, jail_name))

        if db_insert:
            requests.post(
                'https://f2brbl.mailcleaner.net/ip?ip={}&jail={}&host_id={}'.
                format(ip, jail_name,
                       MailCleanerConfig.get_instance().get_value("CLIENTID")))
            ret = self.fail2banDB.insert_row(ip, jail_name)
            if ret == InsertError.BLACKLISTED.value:
                self.__mcLogger.warn("Blacklisting {0} from {1}".format(
                    ip, jail_name))
                self.__safe_run("fail2ban-client set {0}-bl banip {1}".format(
                    jail_name, ip))

    def blacklist(self, ip: str, jail_name: str,
                  db_insert: str = True) -> None:
        if db_insert:
            self.fail2banDB.set_ip_jail_blacklisted(ip, jail_name)
        self.__safe_run("fail2ban-client set {0}-bl banip {1}".format(
            jail_name, ip))

    def unban(self,
              ip: str = None,
              jail_name: str = None,
              db_insert: bool = True,
              f2b_call: bool = False) -> None:
        """ 
            Unban an IP.
        Arguments:
            ip {str} -- ip address
            jail_name {str} -- Jail name
            db_insert {bool} -- Needs to insert to DB,
            f2b_call {bool} -- Needs to call F2B):
        """
        if ip == None:
            ip = self.ip
        if jail_name == None:
            jail_name = self.jail_name
        self.__mcLogger.info("Unban=>{0} inside jail=>{1}".format(
            ip, jail_name))
        if f2b_call:
            self.__safe_run("fail2ban-client set {0} unbanip {1}".format(
                jail_name, ip))
        else:
            if db_insert:
                self.fail2banDB.unban_row(ip, jail_name)

    def __apply_func(self, func, **kwargs) -> None:
        """ Apply the ``func`` with kwargs arguments. The func should be one of Fail2banAction enum.
            Read the dump file, parse it, apply the function on the corresponding jail and delete the file
        
        Arguments:
            func {method} -- In which database to do the action
            **kwargs {???} -- ip address
        """
        try:
            with open(kwargs['file_path'], "r") as file:
                for raw_line in file:
                    ip = raw_line.splitlines()[0]
                    func(ip, kwargs['jail'])
        finally:
            file.close()
            os.remove(kwargs['file_path'])

    def treat_dumps(self) -> None:
        """ This function will parse the dump files found and update the table consequently
            It will delete the files after.
        """
        actions = [(Fail2banAction.TO_ADD, self.ban),
                   (Fail2banAction.TO_UPDATE, self.ban),
                   (Fail2banAction.TO_REMOVE, self.unban),
                   (Fail2banAction.TO_WL, self.whitelist),
                   (Fail2banAction.TO_BL, self.blacklist)]
        jails = self.fail2banDB.get_jails()
        if len(jails) != 0:
            fail2ban_dump_path = self.fail2banDB.get_dump_file_path(
            ) + "dump_fail2ban_"
            for action, func in actions:
                for jail in jails:
                    file_path = fail2ban_dump_path + jail + "_" + action.value
                    if os.path.exists(file_path):
                        self.__apply_func(func, **{
                            'jail': jail,
                            'file_path': file_path
                        })

    def whitelist(self, ip: str, jail_name: str) -> None:
        self.fail2banDB.set_ip_jail_whitelisted(ip, jail_name)
        if not self.__safe_run(
                "fail2ban-client get {0} ignoreip |sed 's/^.*- //'|grep '{1}'".
                format(jail_name, ip),
                hide=True).return_code:
            self.__safe_run("fail2ban-client set {0} addignoreip {1}".format(
                jail_name, ip))
        else:
            print("{0} is already whitelisted in {1}".format(ip, jail_name))

    def reload_fw(self) -> None:
        self.__mcLogger.debug("Reload Firewall called")
        jails = Fail2banJail().all()
        for jail in jails:
            self.__safe_run("iptables -N fail2ban-{0}".format(jail.name))
            self.__safe_run("iptables -A fail2ban-{0} -j RETURN".format(
                jail.name))
            self.__safe_run(
                "iptables -I INPUT -p tcp -m multiport --dports {0} -j fail2ban-{1}"
                .format(jail.port, jail.name))
            self.__safe_run("iptables -N fail2ban-{0}-bl".format(jail.name))
            self.__safe_run("iptables -A fail2ban-{0}-bl -j RETURN".format(
                jail.name))
            self.__safe_run(
                "iptables -I INPUT -p tcp -m multiport --dports {0} -j fail2ban-{1}-bl"
                .format(jail.port, jail.name))
            ips = Fail2banIps.get_all_active_by_jail(jail.name)
            for ip in ips:
                self.__safe_run(
                    "iptables -I fail2ban-{0} 1 -s {1} -j REJECT".format(
                        jail.name, ip.ip))
            bl_ips = Fail2banIps.find_by_blacklisted_and_jail(jail=jail.name)
            for bl_ip in bl_ips:
                self.__safe_run(
                    "iptables -I fail2ban-{0}-bl 1 -s {1} -j REJECT".format(
                        jail.name, bl_ip.ip))
        self.treat_dumps()

    def treat_cron(self) -> None:
        self.__mcLogger.debug("Treat cron called")
        self.__ban_from_mysql()
        self.__unban_from_mysql()
        self.__whitelist_from_mysql()
        self.__blacklist_from_mysql()

    def disable_jail(self, jail_name: str) -> None:
        self.__mcLogger.debug("Disable jail {0}".format(jail_name))
        if MailCleanerConfig.get_instance().get_value("ISMASTER") == "Y":
            Fail2banDB().set_jail_inactive(jail_name)
            Fail2banDB().delete_all_rows_jail(jail_name)
        self.__safe_run("fail2ban-client stop {0}".format(jail_name))

    def enable_jail(self, jail_name: str) -> None:
        self.__mcLogger.debug("Disable jail {0}".format(jail_name))
        Fail2banDB().set_jail_active(jail_name)
        DumpFail2banConfig().dump_jail(jail_name)
        self.__safe_run(
            "fail2ban-client -c {0}/etc/fail2ban/ reload {1}".format(
                MailCleanerConfig.get_instance().get_value("SRCDIR"),
                jail_name))

    def change_config(self, jail_name: str, option: str, value: int) -> None:
        self.__safe_run("fail2ban-client set {0:s} {1:s} {2:d}".format(
            jail_name, option, value),
                        raise_failures=False)
        self.fail2banDB.set_jail_config(jail_name, option, value)

    def disable_blacklist(self, jail_name) -> None:
        self.fail2banDB.disable_blacklist(jail_name)
        self.__safe_run("fail2ban-client stop {0:s}".format(jail_name),
                        raise_failures=False)

    def __ban_from_mysql(self) -> None:
        continu = True
        query_from = 0
        page_size = 10
        jails = Fail2banDB().get_jails()
        for jail in jails:
            ips = Fail2banDB().get_active_jail(jail)
            for ip in ips:
                if self.__safe_run(
                        "fail2ban-client status {0} |grep {1}".format(
                            jail, ip), False, True).return_code:
                    self.__safe_run("fail2ban-client set {0} banip {1}".format(
                        jail, ip))

    def __unban_from_mysql(self) -> None:
        jails = Fail2banDB().get_jails()
        for jail in jails:
            ips = Fail2banDB().get_inactive_jail(jail)
            for ip in ips:
                if not self.__safe_run(
                        "fail2ban-client status {0} |grep {1}".format(
                            jail, ip), False, True).return_code:
                    self.__safe_run(
                        "fail2ban-client set {0} unbanip {1}".format(jail, ip),
                        raise_failures=False)

    def __whitelist_from_mysql(self) -> None:
        jails = Fail2banDB().get_jails()
        for jail in jails:
            ips = Fail2banDB().get_whitelist_jail(jail)
            for ip in ips:
                if self.__safe_run(
                        "fail2ban-client get {0} ignoreip |sed 's/^.*- //'|grep '{1}'"
                        .format(jail, ip),
                        hide=True).return_code:
                    self.__safe_run(
                        "fail2ban-client set {0} addignoreip {1}".format(
                            jail, ip))

    def __blacklist_from_mysql(self) -> None:
        jails = Fail2banDB().get_jails()
        for jail in jails:
            ips = Fail2banDB().get_blacklist_jail(jail)
            for ip in ips:
                if not self.__safe_run(
                        "fail2ban-client status {0}-bl |grep {1}".format(
                            jail, ip), False, True).return_code:
                    self.__safe_run(
                        "fail2ban-client set {0}-bl banip {1}".format(
                            jail, ip),
                        hide=True)

    def __safe_run(self, cmd: str, raise_failures=True, hide=False):
        """
        This function has the responsability to handle results
        and raise an exception if an uknown and unwanted error occured.
        :param cmd: the command to run
        :param raise_failures: Raise exception in case of failure (Exit code different than 0 - Unix exit code)
        :return: Return a Result object http://docs.pyinvoke.org/en/latest/api/runners.html#invoke.runners.Result
        """
        command = run(cmd, warn=True, hide=hide)
        if raise_failures and command.failed:
            raise Fail2banException(
                "An error occured during the run of the command {0} with the following exit_code: {1} \n Stderr: {2}  \n Stdout: {3}"
                .format(command.command, command.return_code, command.stderr,
                        command.stdout))
        return command
