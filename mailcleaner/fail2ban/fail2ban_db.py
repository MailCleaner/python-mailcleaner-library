import subprocess, sys, os
import logging
from enum import Enum
from mailcleaner.db.models.Fail2banJail import Fail2banJail
from mailcleaner.db.models.Fail2banIps import Fail2banIps
from mailcleaner.db.models.Fail2banIps import Fail2banIpsFactory
from sqlalchemy.sql import func
from mailcleaner.config import MailCleanerConfig

log_file = MailCleanerConfig().get_value(
    'VARDIR') + "/log/mc_fail2ban_script.log"
logging.basicConfig(
    filename=log_file,
    filemode='a+',
    format='%(asctime)s - [Fail2banDB] - %(levelname)s - %(message)s',
    datefmt='%d-%b-%y %H:%M:%S')
logging.getLogger().setLevel(logging.INFO)


class Fail2banAction(Enum):
    TO_ADD = "to_add"
    TO_REMOVE = "to_remove"
    TO_UPDATE = "to_update"


class Fail2banDB:
    dump_file_path = ''

    def __init__(self):
        """ 
        Consctructor of the class create the connection to the databases and set dump_file_path
        """
        self.dump_file_path = MailCleanerConfig().get_value('VARDIR') + "/tmp/"

    def get_dump_file_path(self):
        return self.dump_file_path

    def insert_row(self, ip, jail_name):
        """ Check if the row exists in master's Db if not insert it else
            update it
        
        Arguments:
            ip {str} -- ip address
            jail_name {str} -- Jail name
        Returns:
            [int] -- 0 => Created
                     1 => Updated
                     2 => Blacklisted
        """
        return_code = 0
        mc_ban_ip = Fail2banIps().find_by_ip_and_jail(ip, jail_name)
        if mc_ban_ip is not None:
            if not mc_ban_ip.active:
                return_code = self.update_row(ip, jail_name)
        else:
            Fail2banIpsFactory.create(
                ip=ip,
                jail=jail_name,
                host=MailCleanerConfig().get_value('MCHOSTNAME')).save()

        return return_code

    def update_row(self, ip, jail_name):
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
        return_code = 3
        mc_ban_ip = Fail2banIps().find_by_ip_and_jail(ip, jail_name)
        if mc_ban_ip is not None:
            return_code = 1
            mc_ban_ip.active = True
            mc_ban_ip.count += 1
            mc_ban_ip.host = MailCleanerConfig().get_value('MCHOSTNAME')
            mc_ban_ip.last_hit = func.now()
            if (Fail2banJail().find_by_name(jail_name).max_count != -1
                    and mc_ban_ip.count >
                    Fail2banJail().find_by_name(jail_name).max_count):
                mc_ban_ip.blacklisted = True
                return_code = 2
            mc_ban_ip.save()
        return return_code

    def unban_row(self, ip, jail_name):
        """ 
        Set the active column to false in MySql for the couple ip, jail_name
        
        Arguments:
            ip {str} -- ip address
            jail_name {str} -- Jail name
        """
        mc_ban_ip = Fail2banIps().find_by_ip_and_jail(ip, jail_name)
        if mc_ban_ip is not None:
            mc_ban_ip.active = False
            mc_ban_ip.save()

    def set_ip_jail_whitelisted(self, ip, jail_name):
        mc_ban_ip = Fail2banIps().find_by_ip_and_jail(ip, jail_name)
        mc_ban_ip.whitelisted = True
        mc_ban_ip.active = False
        mc_ban_ip.save()

    def get_jails(self):
        jails = []
        row_jails = Fail2banJail.get_jails()
        for row_jail in row_jails:
            jails.append(row_jail.name)
        return jails

    def get_active_jail(self, jail_name):
        ips = []
        raw_ips = Fail2banIps().get_all_active_by_jail(jail_name)
        for raw_ip in raw_ips:
            ips.append(raw_ip.ip)
        return ips

    def get_whitelist_jail(self, jail_name):
        ips = []
        raw_ips = Fail2banIps().find_by_whitelisted_and_jail(jail_name)
        for raw_ip in raw_ips:
            ips.append(raw_ip.ip)
        return ips

    def get_blacklist_jail(self, jail_name):
        ips = []
        raw_ips = Fail2banIps().find_by_blacklisted_and_jail(jail_name)
        for raw_ip in raw_ips:
            ips.append(raw_ip.ip)
        return ips

    def __log_and_dump(self, ip, jail_name, action):
        """Log the error and dump info in files
        
        Arguments:
            ip {str} -- ip address
            jail_name {str} -- Jail name 
            action {str} -- Action to do in mysql
        """
        logging.warning(ip + "=>" + jail_name +
                        " Cannot add/update mysql dumping into file")
        tf = 'dump_fail2ban_' + jail_name + '_' + action
        f = open(self.dump_file_path + tf, 'a+')
        f.write(ip + "\n")
        f.close()
        logging.info("ip wrote into " + tf)
