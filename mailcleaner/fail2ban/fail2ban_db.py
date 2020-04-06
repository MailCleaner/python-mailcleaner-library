import subprocess, sys, os
from enum import Enum
from mailcleaner.db.models.Fail2banJail import Fail2banJail
from mailcleaner.db.models.Fail2banIps import Fail2banIps
from mailcleaner.db.models.Fail2banIps import Fail2banIpsFactory
from sqlalchemy.sql import func
from mailcleaner.config import MailCleanerConfig
from mailcleaner.logger import McLogger
from mailcleaner.network import *
from sqlalchemy.exc import *


class Fail2banAction(Enum):
    TO_ADD = "to_add"
    TO_REMOVE = "to_remove"
    TO_UPDATE = "to_update"
    TO_WL = "to_wl"
    TO_BL = "to_bl"


class InsertError(Enum):
    CREATED = 0
    UPDATED = 1
    BLACKLISTED = 2


class UpdateError(Enum):
    BANNED = 1
    BLACKLISTED = 2
    ERROR = 3


class Fail2banDB:
    dump_file_path = ''
    __mcLogger = None

    def __init__(self):
        """ 
        Constructor of the class create the connection to the databases and set dump_file_path
        """
        self.dump_file_path = MailCleanerConfig().get_value('VARDIR') + "/tmp/"
        self.__mcLogger = McLogger(name="Fail2banDB",
                                   project="fail2ban",
                                   filename="mc-fail2ban")

    def get_dump_file_path(self):
        return self.dump_file_path

    def insert_row(self, ip, jail_name) -> int:
        """ Check if the row exists in master's DB if not insert it else
            update it
        
        Arguments:
            ip {str} -- ip address
            jail_name {str} -- Jail name
        Returns:
            [int] -- 0 => Created
                     1 => Updated
                     2 => Blacklisted
        """
        Enum
        return_code = InsertError.CREATED.value
        try:
            mc_ban_ip = Fail2banIps().find_by_ip_and_jail(ip, jail_name)
        except OperationalError:
            self.__log_and_dump(ip, jail_name, Fail2banAction.TO_ADD.value)
            exit
        if mc_ban_ip is not None:
            if not mc_ban_ip.active:
                return_code = self.update_row(ip, jail_name)
        else:
            test = Fail2banIps(ip=ip,
                               jail=jail_name,
                               host=get_reverse_name(),
                               count=1)
            try:
                test.save()
            except OperationalError:
                self.__log_and_dump(ip, jail_name, Fail2banAction.TO_ADD.value)
                exit
        return return_code

    def update_row(self, ip, jail_name) -> int:
        """
        Update the row in Dbs for couple ip and jail
        and blacklist if > than max_count defined in Fail2banJail
        
        Arguments:
            ip {string} -- ip to select
            jail_name {string} -- jail to select
        
        Returns:
            [int] -- 1 => Banned
                     2 => Blacklisted
                     3 => Error
        """
        return_code = UpdateError.ERROR.value
        try:
            mc_ban_ip = Fail2banIps().find_by_ip_and_jail(ip, jail_name)
        except OperationalError:
            self.__log_and_dump(ip, jail_name, Fail2banAction.TO_UPDATE.value)
            exit
        if mc_ban_ip is not None:
            return_code = UpdateError.BANNED.value
            mc_ban_ip.active = True
            mc_ban_ip.count += 1
            mc_ban_ip.host = get_reverse_name()
            mc_ban_ip.last_hit = func.now()
            if (Fail2banJail().find_by_name(jail_name).max_count != -1
                    and mc_ban_ip.count >
                    Fail2banJail().find_by_name(jail_name).max_count):
                mc_ban_ip.blacklisted = True
                return_code = UpdateError.BLACKLISTED.value
            try:
                mc_ban_ip.save()
            except OperationalError:
                if return_code == UpdateError.BANNED.value:
                    self.__log_and_dump(ip, jail_name,
                                        Fail2banAction.TO_UPDATE.value)
                else:
                    self.__log_and_dump(ip, jail_name,
                                        Fail2banAction.TO_BL.value)
        return return_code

    def unban_row(self, ip: str, jail_name: str) -> None:
        """ 
        Set the active column to false in MySql for the couple ip, jail_name
        Resets the count and blacklisted value
        Arguments:
            ip {str} -- ip address
            jail_name {str} -- Jail name
        """
        try:
            mc_ban_ip = Fail2banIps().find_by_ip_and_jail(ip, jail_name)
        except OperationalError:
            self.__log_and_dump(ip, jail_name, Fail2banAction.TO_REMOVE.value)
        if mc_ban_ip is not None:
            mc_ban_ip.active = False
            mc_ban_ip.blacklisted = False
            try:
                mc_ban_ip.save()
            except OperationalError:
                self.__log_and_dump(ip, jail_name,
                                    Fail2banAction.TO_REMOVE.value)

    def set_ip_jail_blacklisted(self, ip: str, jail_name: str):
        try:
            bl_ip = Fail2banIps().find_by_ip_and_jail(ip, jail_name)
        except OperationalError:
            self.__log_and_dump(ip, jail_name, Fail2banAction.TO_WL.value)
        if bl_ip is not None:
            bl_ip.blacklisted = True
            bl_ip.active = True
            bl_ip.save()
        else:
            bl_ip = Fail2banIps(ip=ip,
                                active=False,
                                jail=jail_name,
                                host=get_reverse_name(),
                                count=0,
                                blacklisted=True)
            try:
                bl_ip.save()
            except OperationalError:
                self.__log_and_dump(ip, jail_name, Fail2banAction.TO_WL.value)

    def set_ip_jail_whitelisted(self, ip: str, jail_name: str):
        try:
            wl_ip = Fail2banIps().find_by_ip_and_jail(ip, jail_name)
        except OperationalError:
            self.__log_and_dump(ip, jail_name, Fail2banAction.TO_WL.value)
        if wl_ip is not None:
            wl_ip.whitelisted = True
            wl_ip.active = False
            wl_ip.save()
        else:
            wl_ip = Fail2banIps(ip=ip,
                                active=False,
                                jail=jail_name,
                                host=get_reverse_name(),
                                count=0,
                                whitelisted=True)
            try:
                wl_ip.save()
            except OperationalError:
                self.__log_and_dump(ip, jail_name, Fail2banAction.TO_WL.value)

    def set_jail_inactive(self, jail_name: str) -> None:
        mc_jail = Fail2banJail().find_by_name(jail_name)
        mc_jail.enabled = False
        mc_jail.save()

    def set_jail_active(self, jail_name: str) -> None:
        mc_jail = Fail2banJail().find_by_name(jail_name)
        mc_jail.enabled = True
        mc_jail.save()

    def set_jail_config(self, jail_name: str, option: str, value: int) -> None:
        mc_jail = Fail2banJail().find_by_name(jail_name)
        if option == "findtime":
            mc_jail.findtime = value
        elif option == "bantime":
            mc_jail.bantime = value
        elif option == "maxretry":
            mc_jail.maxretry = value
        mc_jail.save()

    def get_jails(self):
        jails = []
        row_jails = Fail2banJail.get_jails()
        for row_jail in row_jails:
            jails.append(row_jail.name)
        return jails

    def get_active_jail(self, jail_name: str):
        ips = []
        raw_ips = Fail2banIps().get_all_active_by_jail(jail_name)
        for raw_ip in raw_ips:
            ips.append(raw_ip.ip)
        return ips

    def get_inactive_jail(self, jail_name: str):
        ips = []
        raw_ips = Fail2banIps().get_all_active_by_jail(jail_name, active=False)
        for raw_ip in raw_ips:
            ips.append(raw_ip.ip)
        return ips

    def get_whitelist_jail(self, jail_name: str):
        ips = []
        raw_ips = Fail2banIps().find_by_whitelisted_and_jail(jail_name)
        for raw_ip in raw_ips:
            ips.append(raw_ip.ip)
        return ips

    def get_blacklist_jail(self, jail_name: str):
        ips = []
        raw_ips = Fail2banIps().find_by_blacklisted_and_jail(jail_name)
        for raw_ip in raw_ips:
            ips.append(raw_ip.ip)
        return ips

    def check_blacklisted(self, ip, jail_name: str) -> bool:
        return Fail2banIps().find_by_blacklisted_and_jail(
            jail_name) is not None

    def disable_blacklist(self, jail_name: str):
        jail = Fail2banJail().find_by_name(jail_name)
        jail.max_count = -1
        jail.save()
        ips = Fail2banIps().find_by_blacklisted_and_jail(jail_name, True)
        for ip in ips:
            ip.delete()

    def delete_all_rows_jail(self, jail_name: str):
        return Fail2banIps().reset_jail_ips(jail_name)

    def __log_and_dump(self, ip, jail_name: str,
                       action: Fail2banAction) -> None:
        """Log the error and dump info in files
        
        Arguments:
            ip {str} -- ip address
            jail_name {str} -- Jail name 
            action {str} -- Action to do in mysql
        """
        self.__mcLogger.warn(
            "{0}=>{1} Cannot add/update mysql dumping into file".format(
                ip, jail_name))
        tf = 'dump_fail2ban_' + jail_name + '_' + action
        f = open(self.dump_file_path + tf, 'a+')
        f.write(ip + "\n")
        f.close()
        self.__mcLogger.info("ip wrote into {0}".format(tf))
