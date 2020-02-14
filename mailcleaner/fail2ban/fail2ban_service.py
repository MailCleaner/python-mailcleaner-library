#!/usr/bin/python
import subprocess, sys, os
import logging
try:
    from mailcleaner.config import MailCleanerConfig
    from .fail2ban_db import Fail2banDB
    from .fail2ban_db import Fail2banAction
    from mailcleaner.logger import McLogger
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
    port = ''
    ip_type = 'IPV4'
    fail2banDB = None
    __mcLogger = None

    def __init__(self, jail_name: str = '', ip: str = '', port: str = ''):
        self.jail_name = jail_name
        self.ip = ip
        self.port = port
        self.fail2banDB = Fail2banDB()
        self.__mcLogger = McLogger(
            name="Fail2banService", project="fail2ban", filename="mc-fail2ban")

    def set_ip(self, ip: str):
        self.ip = ip

    def __str__(self) -> str:
        return "jail: " + self.jail_name + " ip:" + self.ip + " port: " + self.port

    def set_port(self, port: str):
        self.port = port

    def set_jail_name(self, jail_name: str):
        self.jail_name = jail_name

    def ban(self,
            ip=None,
            jail_name=None,
            port=None,
            db_insert=True,
            f2b_call=False):
        """ 
            Ban an IP.
            Blacklist the IP, if it needs to
        Arguments:
            ip {str} -- ip address
            jail_name {str} -- Jail name
            port {str} -- Ports,
            db_insert {bool} -- Needs to insert to DB,
            f2b_call {bool} -- Needs to call F2B):
        """
        if ip == None:
            ip = self.ip
        if jail_name == None:
            jail_name = self.jail_name

        if f2b_call:
            self.__safe_run(
                "fail2ban-client set {} banip {}".format(jail_name, ip))

        self.__mcLogger.info(
            "Banning=>{} inside jail=>{}".format(ip, jail_name))

        if db_insert:
            ret = self.fail2banDB.insert_row(ip, jail_name)
            if ret == 2:
                self.__mcLogger.warn(
                    "Blacklisting {} from {}".format(ip, jail_name))
                self.__safe_run(
                    "fail2ban-client set {}-bl banip {}".format(jail_name, ip))

    def unban(self, ip=None, jail_name=None, db_insert=True, f2b_call=False):
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
        self.__mcLogger.info("Unban=>" + ip + " inside jail=>" + jail_name)
        if f2b_call:
            self.__safe_run(
                "fail2ban-client set {} unbanip {}".format(jail_name, ip))
        else:
            if db_insert:
                self.fail2banDB.unban_row(ip, jail_name)

    def __apply_func(self, func, **kwargs):
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

    def treat_dumps(self):
        """ This function will parse the dump files found and update the table consequently
            It will delete the files after.
        """
        actions = [(Fail2banAction.TO_ADD,
                    self.ban), (Fail2banAction.TO_UPDATE, self.ban),
                   (Fail2banAction.TO_REMOVE, self.unban)]
        jails = self.fail2banDB.get_jails()
        if len(jails) != 0:
            fail2ban_dump_path = self.fail2banDB.get_dump_file_path(
            ) + "dump_fail2ban_"
            for action, func in actions:
                for jail in jails:
                    file_path = fail2ban_dump_path + jail + "_" + action.value
                    if os.path.exists(file_path):
                        self.__apply_func(
                            func, **{'jail': jail,
                                     'file_path': file_path})

    def whitelist(self, ip, jail_name):
        self.fail2banDB.set_ip_jail_whitelisted(ip, jail_name)
        self.__safe_run(
            "fail2ban-client set {} addignoreip {}".format(jail_name, ip))

    def reload_fw(self):
        self.__mcLogger.debug("Reload Firewall called")
        self.treat_dumps()
        self.__ban_from_mysql()
        self.__blacklist_from_mysql()

    def treat_cron(self):
        self.__mcLogger.debug("Treat cron called")
        self.__ban_from_mysql()
        self.__whitelist_from_mysql()
        self.__blacklist_from_mysql()

    def disable_jail(self, jail_name):
        self.__mcLogger.debug("Disable jail {}".format(jail_name))
        self.__safe_run("clear")
        if MailCleanerConfig.get_instance().get_value("ISMASTER") == "Y":
            Fail2banDB().set_jail_inactive(jail_name)
            Fail2banDB().delete_all_rows_jail(jail_name)
        self.__safe_run("fail2ban-client stop {}".format(jail_name))

    def __ban_from_mysql(self):
        continu = True
        query_from = 0
        page_size = 10
        jails = Fail2banDB().get_jails()
        for jail in jails:
            ips = Fail2banDB().get_active_jail(jail)
            for ip in ips:
                self.__safe_run(
                    "fail2ban-client set {} banip {}".format(jail, ip))

    def __whitelist_from_mysql(self):
        jails = Fail2banDB().get_jails()
        for jail in jails:
            ips = Fail2banDB().get_whitelist_jail(jail)
            for ip in ips:
                self.__safe_run(
                    "fail2ban-client set {} addignoreip {}".format(jail, ip))

    def __blacklist_from_mysql(self):
        jails = Fail2banDB().get_jails()
        for jail in jails:
            ips = Fail2banDB().get_blacklist_jail(jail)
            for ip in ips:
                self.__safe_run(
                    "fail2ban-client set {}-bl banip {}".format(jail, ip))

    def __safe_run(self, cmd: str, raise_failures=True):
        """
        This function has the responsability to handle results
        and raise an exception if an uknown and unwanted error occured.
        :param cmd: the command to run
        :param raise_failures: Raise exception in case of failure (Exit code different than 0 - Unix exit code)
        :return: Return a Result object http://docs.pyinvoke.org/en/latest/api/runners.html#invoke.runners.Result
        """
        command = run(cmd, warn=True)
        if raise_failures and command.failed:
            raise Fail2banException(
                "An error occured during the run of the command " +
                command.command + " with the following exit_code: " +
                str(command.return_code) + "\n Stderr: " + str(command.stderr)
                + " \n Stdout: " + str(command.stdout))
        return command
