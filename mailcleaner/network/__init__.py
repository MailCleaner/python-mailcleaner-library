import logging
import re

from invoke import run

from mailcleaner.config import MailCleanerConfig
from mailcleaner.db.models import SystemConf

_mc_config = MailCleanerConfig.get_instance()
system_conf = SystemConf.first()


def get_qualify_domain() -> str:
    """
    Define the qualify domain used by MailCleaner. This value is defined by first looking at the default_domain
    configured by the administrator of MailCleaner. If nothing is configured then we will get this value by looking
    at the hostname.
    :return: the qualified domain of this MailCleaner host
    """
    qualify_domain = ""
    logging.debug("default_domain = ".format(
        system_conf.default_domain))
    if "^" not in system_conf.default_domain or "*" not in system_conf.default_domain:
        qualify_domain = system_conf.default_domain
    else:
        qualify_domain_result = run("/bin/hostname --fqdn",
                                    hide=True,
                                    warn=True)
        if qualify_domain_result.ok:
            qualify_domain = qualify_domain_result.stdout
            if qualify_domain == "":
                qualify_domain = _mc_config.get_value("DEFAULTDOMAIN")
        else:
            logging.error(
                "An error occured in getting helo name: {}".format(
                    qualify_domain_result.stderr))
            exit(255)
    logging.debug("Qualify domain: {}".format(qualify_domain))
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
            result = run(
                "/sbin/ifconfig | /bin/grep 'inet addr' | /bin/grep -v '127.0.0.1'",
                hide=True,
                warn=True)
            if result.ok:
                inet_adr_search = re.search('inet addr:([0-9.]+)',
                                            result.stdout, re.IGNORECASE)
                if inet_adr_search:
                    helo_name = inet_adr_search.group(1)
                logging.debug(
                    "Found helo name: {}".format(inet_adr_search))
            else:
                logging.error(
                    "An error occured in getting helo name: {}".format(
                        result.stderr))
                exit(255)
        mailcleaner_config = MailCleanerConfig.get_instance()
        mailcleaner_config.change_configuration("HELONAME", helo_name)

    logging.debug("Helo name: {}".format(helo_name))

    return helo_name
