#!/usr/bin/env python3
import logging
import re
import netifaces
import socket

from invoke import run

from mailcleaner.config import MailCleanerConfig
from mailcleaner.db.models import SystemConf
from mailcleaner.logger import McLogger

_mc_config = MailCleanerConfig.get_instance()
system_conf = SystemConf.first()
_mcLogger = McLogger(name="Network")


def get_qualify_domain() -> str:
    """
    Define the qualify domain used by MailCleaner. This value is defined by first looking at the default_domain
    configured by the administrator of MailCleaner. If nothing is configured then we will get this value by looking
    at the hostname.
    :return: the qualified domain of this MailCleaner host
    """
    qualify_domain = ""
    _mcLogger.debug("default_domain = ".format(system_conf.default_domain))
    if "^" not in system_conf.default_domain or "*" not in system_conf.default_domain:
        qualify_domain = system_conf.default_domain
    else:
        qualify_domain = socket.gethostname()
        if qualify_domain == "":
            qualify_domain = _mc_config.get_value("DEFAULTDOMAIN")
        else:
            _mcLogger.error("An error occured in getting helo name: {}".format(
                qualify_domain_result.stderr))
            exit(255)
    _mcLogger.debug("Qualify domain: {}".format(qualify_domain))
    return qualify_domain


def get_helo_name() -> str:
    """
    Determine the HELO_NAME used by Exim for SMTP session.
    The HELO_NAME can be set in different ways. First, we look if the MailCleaner Configuration file contains this
    parameter and consider it if it's exists. Otherwise, we will look at qualify_domain and finally getting the
    inet address via ifconfig.
    :return: the helo_name of this MailCleaner host
    """
    if _mc_config.get_value("HELONAME") is not "":
        helo_name = _mc_config.get_value("HELONAME")
    else:
        helo_name = get_qualify_domain()
        if "." not in helo_name:
            try:
                helo_name = netifaces.ifaddresses('eth0')[
                    netifaces.AF_INET][0]['addr']
                _mcLogger.debug("Found helo name: {}".format(helo_name))

            except Exception as e:
                _mcLogger.error(
                    "An error occured in getting helo name: {}".format(e))
                exit(255)

        mailcleaner_config = MailCleanerConfig.get_instance()
        mailcleaner_config.change_configuration("HELONAME", helo_name)
        _mcLogger.debug("mailcleaner.network - HELONAME: {}".format(
            mailcleaner_config.get_value("HELONAME")))

    _mcLogger.debug("Helo name: {}".format(helo_name))
    return helo_name


def get_reverse_name() -> str:
    """
    Determine the revered dns name of the ip
    :return: the revered dns result of this MailCleaner host
    """
    reversed_ip = ''
    try:
        reversed_ip = socket.gethostbyaddr(
            netifaces.ifaddresses('eth0')[netifaces.AF_INET][0]['addr'])[0]
        _mcLogger.debug("Reversed name: {}".format(reversed_ip))
    except Exception as e:
        _mcLogger.error(
            "An error occured in resolving reversed ip: {}".format(e))
    return reversed_ip


def get_interfaces() -> list:
    interfaces = run("ls -h /sys/class/net/ | sed 's/^.*\///'",
                     hide=True).stdout.split('\n')
    interfaces = [i for i in interfaces if i]
    return interfaces