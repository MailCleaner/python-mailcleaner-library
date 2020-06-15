#!/usr/bin/env python
import click
import os
import socket
import re
from mailcleaner.fail2ban.fail2ban_service import Fail2banService
import ipaddress
import netifaces as ni
from mailcleaner.network import *
from mailcleaner.db.models import Slave
from email.utils import parseaddr
from sys import exit


@click.group()
def cli():
    """Api to use fail2ban within MailCleaner"""
    pass


@cli.command(short_help='Ban an IP')
@click.option('-j', '--jail', required=True, help='Fail2Ban jail name')
@click.option('-i', '--ip', required=True, help='IP to ban')
@click.option('--f2b-call/--no-f2b-call',
              default=False,
              help="Call Fail2ban, default False")
@click.option('--db-insert/--no-db-insert',
              default=True,
              help="Insert into DB, default True")
def ban(jail, ip, db_insert, f2b_call):
    """
    Ban an IP
    """
    if "/" in ip:
        ip_address = None
        try:
            ip_address = ipaddress.IPv4Network(ip)
        except ipaddress.AddressValueError as err:
            print(err)
            exit(1)
        for interface in get_interfaces():
            int_ip = ni.ifaddresses(interface)[ni.AF_INET][0]['addr']
            if ipaddress.IPv4Network(int_ip).network_address in ip_address:
                print("You can't ban your own network")
                exit(1)
        slaves = Slave().get_all_slaves()
        for slave in slaves:
            slave_ip = slave.hostname
            if re.search('[a-zA-Z]', slave_ip):
                slave_ip = socket.gethostbyname(slave_ip)
            if ipaddress.IPv4Network(slave_ip).network_address in ip_address:
                print("You can't ban the network of one of your slave")
                exit(1)
        if int(ip.split("/")[1]) <= 24:
            if not click.confirm(
                    "Are you sure that you want to ban {0:,} ips".format(
                        ip_address.num_addresses)):
                exit(0)
    else:
        ip_address = None
        try:
            ip_address = ipaddress.IPv4Address(ip)
        except ipaddress.AddressValueError as err:
            print(err)
            exit(1)
        for interface in get_interfaces():
            int_ip = ni.ifaddresses(interface)[ni.AF_INET][0]['addr']
            if ipaddress.IPv4Address(int_ip) == ip_address:
                print("You can't ban your own ip")
                exit(1)
        slaves = Slave().get_all_slaves()
        for slave in slaves:
            slave_ip = slave.hostname
            if re.search('[a-zA-Z]', slave_ip):
                slave_ip = socket.gethostbyname(slave_ip)
            if ipaddress.IPv4Address(slave_ip) == ip_address:
                print("You can't ban the ip of one of your slave")
                exit(1)

    cur = Fail2banService(jail_name=jail, ip=str(ip_address))
    cur.ban(f2b_call=f2b_call, db_insert=db_insert)


@cli.command(short_help='Unban specified IP in the jail')
@click.option('-j', '--jail', required=True, help='Fail2Ban jail name')
@click.option('-i', '--ip', required=True, help='IP to unban')
@click.option('--f2b-call/--no-f2b-call',
              default=False,
              help="Call Fail2ban, default False")
@click.option('--db-insert/--no-db-insert',
              default=True,
              help="Insert into DB, default True")
def unban(jail, ip, db_insert, f2b_call):
    """
    Unban specified IP in the jail
    """
    f2b = Fail2banService(jail_name=jail, ip=ip)
    f2b.unban(f2b_call=f2b_call, db_insert=db_insert)


@click.group()
def internal():
    """
        Internal group for click commands
    """
    pass


@internal.command(
    short_help='Option called after the reload of MailCleaner. Don\'t use it')
@click.argument('hidden', default='')
def reload_fw(hidden):
    """ 
        It will read MySQL and ban in iptable each row that are currently active or blacklisted in DB \n
        Treat each dumps in VARDIR/tmp
    """
    f2b = Fail2banService()
    if hidden == 'firewall':
        f2b.reload_fw()


@internal.command(short_help='Ban in iptable all rows present in DB')
def fetch_db():
    """
    It will read MySQL and ban in iptable each row that 
    are currently active or blacklisted in DB
    Treat each dumps in VARDIR/tmp
    """
    f2b = Fail2banService()
    f2b.reload_fw()


@internal.command(short_help='Option called by cron jobs.')
def cron_job():
    """
        It will read MySQL and ban in iptable each row that are currently active or blacklisted in DB \n
        Used to update iptables with rows added by the replication"""
    f2b = Fail2banService()
    f2b.treat_cron()


@internal.command(short_help="Command used to send ip to RBL")
@click.argument('jail')
@click.argument('ip')
def send_rbl(jail, ip):
    f2b = Fail2banService()
    f2b.notify_rbl(jail, ip)


@click.group()
def mail():
    """
    Mail configuration of Fail2Ban
    """
    pass


@mail.command('dest', short_help="Configure the destination email address")
@click.option('-e', '--email', help="Destination email address")
def mail_dest(email: str):
    """
        Change destination mail for Fail2ban
    """
    if '@' in parseaddr(email)[1]:
        f2b = Fail2banService()
        f2b.change_dest_email(email)


@mail.command('src', short_help="Configure the source email address")
@click.option('-e',
              '--email',
              default="fail2ban@yourservername",
              help="Source email address",
              show_default=True)
def mail_src(email: str):
    """
        Change the source email address of Fail2Ban
    """
    if '@' in parseaddr(email)[1]:
        f2b = Fail2banService()
        f2b.change_src_email(email)


@mail.command('name',
              short_help="Configure the display name of the email address")
@click.option('-n',
              '--name',
              default="[MailCleaner] Fail2Ban",
              help="Display name",
              show_default=True)
def mail_name(name: str):
    """
        Change the display name of the source email address of Fail2Ban
    """
    f2b = Fail2banService()
    f2b.change_src_name(name)


@mail.command('modify',
              short_help="Modify the send mail action for all blacklist jail")
@click.option('--send/--no-send', default=True)
def mail_modify(send):
    """
        Disable/Enable the send mail action for all blacklist  jail
    """
    f2b = Fail2banService()
    f2b.modify_all_send_mail(send)


@click.group()
def general():
    """
    General configuration of Fail2Ban
    """
    pass


@general.command('enable', short_help="Enable all jails")
def gen_enable():
    """
        Enable all jails
    """
    f2b = Fail2banService()
    f2b.enable_all_jail()


@general.command('disable', short_help="Enable all jails")
def gen_disable():
    """
        Disable all jails
    """
    f2b = Fail2banService()
    f2b.disable_all_jails()


@general.command('disable-bl', short_help="Disable blacklist for all jails")
def gen_disable_bl():
    """
        Disable all blacklist jails
    """
    f2b = Fail2banService()
    f2b.disable_all_blacklist()


@general.command('enable-bl', short_help="Enable blacklist for all jails")
@click.option('-v',
              '--value',
              default=3,
              help="Max number of ban before blacklist",
              show_default=True)
def gen_enable_bl(value: int):
    """
        Enable all blacklist jails<
    """
    if value > 1:
        f2b = Fail2banService()
        f2b.enable_all_blacklist(value)


@click.group()
def whitelist():
    """
        Whitelist group for click commands
    """
    pass


@whitelist.command('add')
@click.option('-j', '--jail', required=True, help='Fail2Ban jail name')
@click.option('-i', '--ip', required=True, help='IP to unban')
def wl_add(jail, ip):
    """
    Whitelist specified IP in the jail
    """
    f2b = Fail2banService(jail_name=jail, ip=ip)
    f2b.whitelist(ip, jail)


@whitelist.command('remove')
@click.option('-j', '--jail', required=True, help='Fail2Ban jail name')
@click.option('-i', '--ip', required=True, help='IP to unban')
def wl_remove(jail, ip):
    """
    Remove specified IP in the jail's whitelist
    """
    f2b = Fail2banService(jail_name=jail, ip=ip)
    f2b.remove_from_whitelist(ip, jail)


@click.group()
def blacklist():
    """
        Blacklist group for click commands
    """


@blacklist.command('disable',
                   short_help='Disable blacklist for specified jail')
@click.option('-j', '--jail', required=True, help='Fail2Ban jail name')
def bl_disable(jail):
    """
        Disable blacklist for specified jail

        Note : Don't add "-bl" for the jail name 
    """
    f2b = Fail2banService()
    f2b.disable_blacklist(jail)


@blacklist.command('enable', short_help='Enable blacklist for specified jail')
@click.option('-j', '--jail', required=True, help='Fail2Ban jail name')
@click.option('-v',
              '--value',
              default=3,
              help="Max number of ban before blacklist",
              show_default=True)
def bl_enable(jail, value):
    """
        Enable blacklist for specified jail
        
        \b
        Note:
                Don't add "-bl" for the jail name
                Fail2ban needs to be restarted
    """
    f2b = Fail2banService()
    f2b.enable_blacklist(jail, value)


@blacklist.command('add',
                   short_help='Add IP in the blacklist for specified jail')
@click.option('-j', '--jail', required=True, help='Fail2Ban jail name')
@click.option('-i', '--ip', required=True, help='IP to blacklist')
def bl_add(jail, ip):
    """
        Add IP in the blacklist for specified jail
        Note : Don't add "-bl" for the jail name 
    """
    f2b = Fail2banService()
    f2b.blacklist(jail_name=jail, ip=ip, blacklisted=True)


@blacklist.command('remove',
                   short_help='Remove IP in the blacklist for specified jail')
@click.option('-j', '--jail', required=True, help='Fail2Ban jail name')
@click.option('-i', '--ip', required=True, help='IP to unblacklist')
def bl_remove(jail, ip):
    """
        Remove IP in the blacklist for specified jail
    """
    f2b = Fail2banService()
    f2b.blacklist(jail_name=jail, ip=ip, blacklisted=False)


@click.group()
def jail():
    """
        Jail group for click commands
    """


jail.add_command(bl_disable, 'disable-bl')


@jail.command('enable', short_help='Enable the corresponding jail')
@click.option('-j', '--jail', required=True, help='Fail2Ban jail name')
def enable_jail(jail):
    """
        Start the corresponding jail, doesn't work for blacklist specific jail
    """
    f2b = Fail2banService()
    f2b.enable_jail(jail)


@jail.command(
    'modify-mail',
    short_help='Change configuration of the corresponding jail for send mail')
@click.option('-j', '--jail', required=True, help='Fail2Ban jail name')
@click.option('--send/--no-send', default=True)
def modify_mail(jail, send):
    """
        Modify the behaviour of the send mail action for blacklist jail
    """
    f2b = Fail2banService()
    f2b.modify_send_mail(jail, send)


@jail.command('change', short_help='Change configuration of specified jail.')
@click.option('-j', '--jail', required=True, help='Fail2Ban jail name')
@click.option('--option',
              type=click.Choice(['findtime', 'bantime', 'maxretry'],
                                case_sensitive=False),
              required=True)
@click.option('-v',
              '--value',
              required=True,
              help='Time in second or number of max retry',
              type=int)
def change_config(jail, option, value):
    """
        For findtime and bantime, the value is in second \n
        For maxretry it is the number of time, that an IP needs to appear, to be banned
    """
    f2b = Fail2banService()
    f2b.change_config(jail, option, value)


@jail.command('reload', short_help="Reload the corresponding jail")
@click.option('-j', '--jail', required=True, help='Fail2Ban jail name')
def reload_jail(jail):
    f2b = Fail2banService()
    f2b.reload_jail(jail)
    print()


@jail.command('disable', short_help='Disable the corresponding jail')
@click.option('-j', '--jail', required=True, help='Fail2Ban jail name')
def disable_jail(jail):
    """
        If you are on a master, it will delete all non whitelisted ips and disable the jail
        otherwise will just disable the jail
    """
    f2b = Fail2banService()
    f2b.disable_jail(jail)


@jail.command('list', short_help='List IPs banned in DB')
@click.option('-j', '--jail', required=True, help='Fail2Ban jail name')
def ip_list(jail):
    print()


cli.add_command(whitelist)
cli.add_command(blacklist)
cli.add_command(jail)
cli.add_command(internal)
cli.add_command(general)
cli.add_command(mail)
if __name__ == "__main__":
    cli()
