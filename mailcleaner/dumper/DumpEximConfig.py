#!/usr/bin/env python3
import logging
import os
import re

from invoke import run

from mailcleaner.db.models import SystemConf, MTAConfig, AntiSpam, HTTPDConfig, DnsList
from mailcleaner.dumper.MailCleanerBaseDump import MailCleanerBaseDump

# Disable invoke library logging noise
from mailcleaner.network import get_helo_name, get_interfaces, is_ipv6_disabled
from mailcleaner.rbl import MailCleanerRBL
logger = logging.getLogger("invoke")
logger.setLevel(logging.ERROR)


class DumpEximConfig(MailCleanerBaseDump):

    _mc_config = MailCleanerConfig.get_instance()
    system_conf = SystemConf.first()

    def dump(self) -> None:
        """
        Dump all exim stages configuration files.
        """
        self.dump_exim_stage_1()
        self.dump_exim_stage_2()
        self.dump_exim_stage_4()

    def dump_exim_stage_1(self) -> None:
        """
        Dump exim_stage1 configuration file.
        """
        """
        rbl part too complicated right now: Line ~720 in dumper exim
        debug need to be in yaml
        """
        exim_stage_1 = MTAConfig.find_by_set_id_and_stage_id(set_id=1,
                                                             stage_id=1)
        httdp_config = HTTPDConfig.first()
        antispam = AntiSpam.first()
        ad_basedn, ad_binddn, ad_pass = self.system_conf.ad_param.split(':')
        disable_ipv6 = True
        for interface in network.get_interfaces():
            if not network.is_ipv6_disabled(interface):
                disable_ipv6 = False
                break

        rbls = exim_stage_1.rbls.split(' ')
        rbls_dns_name = ()
        if rbls[0] != '':
            mailcleaner_rbl = MailCleanerRBL(
                "{}/etc/rbls/".format(_mc_config.get_value('SRCDIR')), rbls)
            rbls_path = "{}/etc/rbls".format(_mc_config.get_value('SRCDIR'))
            for rbl in rbls:
                if mailcleaner_rbl.check_valid_rbl_dnsname(rbls_path, rbl):
                    rbls.remove(rbl)
                else:
                    rbls_dns_name.append(
                        mailcleaner_rbl.get_value(rbl, 'dnsname'))

        rbl = True if rbls[0] != '' else False

        bs_rbls = exim_stage_1.bs_rbls.split(' ')
        bs_rbls_dns_name = ()
        if bs_rbls[0] != '':
            mailcleaner_bs_rbl = MailCleanerRBL(
                "{}/etc/rbls/".format(_mc_config.get_value('SRCDIR')), bs_rbls)
            bs_rbls_path = "{}/etc/rbls".format(_mc_config.get_value('SRCDIR'))
            for bs_rbl in bs_rbls:
                if mailcleaner_rbl.check_valid_rbl_dnsname(rbls_path, rbl):
                    rbs_bls.remove(rbl)
                else:
                    bs_rbls_dns_name.append(
                        mailcleaner_rbl.get_value(rbl, 'dnsname'))

        bs_rbl = True if rbls[0] != '' else False
        self.dump_template(
            template_config_src_file='etc/exim/exim_stage1.conf_template',
            config_datas={
                "VARDIR":
                self._mc_config.get_value("VARDIR"),
                "SRCDIR":
                self._mc_config.get_value("SRCDIR"),
                "ad_basedn":
                ad_basedn,
                "ad_binddn":
                ad_binddn,
                "ad_pass":
                ad_pass,
                "ad_server":
                self.system_conf.ad_server,
                "allow_mx_to_ip":
                exim_stage_1.allow_mx_to_ip,
                "archiver_host":
                self.system_conf.archiver_host.split(':')[0],
                "archiver_port":
                self.system_conf.archiver_host.split(':')[1],
                "bsrbl":
                bs_rbl,
                "bsrbls":
                bs_rbls,
                "callout_timeout":
                exim_stage_1.callout_timeout,
                "dmarc_reporting":
                exim_stage_1.dmarc_enable_reports,  # DMARCREPORTING
                "debug":
                False,
                "disable_ipv6":
                disable_ipv6,
                "errors_reply_to":
                exim_stage_1.errors_reply_to,
                "forbid_clear_auth":
                exim_stage_1.forbid_clear_auth,  # FORBIDCLEARAUTH
                "global_max_msg_size":
                exim_stage_1.global_msg_max_size,  # GLOBAL_MAXMSGSIZE
                "helo_name":
                get_helo_name(),
                "hosts_require_incoming_tls":
                exim_stage_1.hosts_require_incoming_tls,
                "hosts_require_tls":
                exim_stage_1.hosts_require_tls.encode('utf-8').split('\r\n'),
                "mask_relay":
                exim_stage_1.mask_relayed_ip,  # MASKRELAY
                "masquerade_outgoing_helo":
                exim_stage_1.masquerade_outgoing_helo,
                "max_rcpt":
                exim_stage_1.max_rcpt,
                "no_ratelimit_hosts":
                exim_stage_1.no_ratelimit_hosts.encode('utf-8').split("\r\n"),
                "outgoing_virus_scan":
                exim_stage_1.outgoing_virus_scan,  # OUTGOINGVIRUSSCAN
                "prevent_relay_from_unknown_domain":
                exim_stage_1.
                allow_relay_for_unknown_domains,  # PREVENTRELAYFROMUNKNOWNDOMAIN
                "qualify_recipient":
                self.system_conf.sysadmin,
                "ratelimit":
                exim_stage_1.ratelimit_enable,
                "ratelimit_rule":
                exim_stage_1.ratelimit_rule,
                "ratelimit_delay":
                exim_stage_1.ratelimit_delay,
                "rbls_after_rcpt":
                exim_stage_1.rbls_after_rcpt,  # RCPTRBL
                "rbl":
                rbl,
                "rbls":
                rbls,
                "rbl_timeout":
                exim_stage_1.rbls_timeout,
                "received_header_max":
                exim_stage_1.received_headers_max,  # __MAX_RECEIVED__
                "reject_bad_spf":
                exim_stage_1.reject_bad_spf,  # REJECTBADSPF
                "reject_bad_rdns":
                exim_stage_1.reject_bad_rdns,  # REJECTBADRDNS
                "reject_dmarc":
                exim_stage_1.dmarc_follow_reject_policy,  # REJECTDMARC
                "relay_from_hosts":
                exim_stage_1.relay_from_hosts.encode('utf-8').split("\r\n"),
                "retry_rule":
                exim_stage_1.retry_rule,
                "verify_sender":
                exim_stage_1.verify_sender,  # SENDERVERIFY
                "smtp_accept_max":
                exim_stage_1.smtp_accept_max,
                "smtp_accept_max_per_trusted_host":
                exim_stage_1.smtp_accept_max_per_trusted_host,
                "smtp_accept_max_per_connection":
                exim_stage_1.smtp_accept_max_per_connection,
                "smtp_accept_max_per_host":
                exim_stage_1.smtp_accept_max_per_host,
                "smtp_banner":
                exim_stage_1.smtp_banner,
                "smtp_conn_access":
                exim_stage_1.smtp_conn_access,
                "smtp_enforce_sync":
                exim_stage_1.smtp_enforce_sync,
                "smtp_load_reserve":
                exim_stage_1.smtp_load_reserve,
                "smtp_receive_timeout":
                exim_stage_1.smtp_receive_timeout,
                "smtp_reserve":
                exim_stage_1.smtp_reserve,
                "syslog_enabled":
                'syslog : ' if exim_stage_1.use_syslog else
                None,  # __IF_USE_SYSLOGENABLED__
                "trusted_hosts":
                antispam.trusted_ips.decode("utf-8").split('\r\n'),
                "trusted_ratelimit":
                exim_stage_1.trusted_ratelimit_enable,
                "trusted_ratelimit_rule":
                exim_stage_1.trusted_ratelimit_rule,
                "trusted_ratelimit_delay":
                exim_stage_1.trusted_ratelimit_delay,
                "use_archiver":
                self.system_conf.use_archiver,  # USEARCHIVER
                "use_tls_smtp_port":
                exim_stage_1.tls_use_ssmtp_port,  # USESSMTPPORT
                "use_tls":
                exim_stage_1.use_incoming_tls,  # USETLS          
                "use_syslog":
                "syslog_facility = local1\nsyslog_processname = stage1"
                if exim_stage_1.use_syslog else
                "#no syslog_facility",  # __IF_USE_SYSLOG__
            })
        pass

    def dump_exim_stage_2(self) -> None:
        """
        Dump exim_stage2 configuration file.
        """
        exim_stage_2 = MTAConfig.find_by_set_id_and_stage_id(set_id=1,
                                                             stage_id=2)
        self.dump_template(
            template_config_src_file='etc/exim/exim_stage2.conf_template',
            config_datas={
                "VARDIR": self._mc_config.get_value("VARDIR"),
                "SRCDIR": self._mc_config.get_value("SRCDIR"),
                "helo_name": get_helo_name(),
                "qualify_recipient": self.system_conf.sysadmin,
                "usetls": exim_stage_2.use_incoming_tls,
                "ignore_bounce_error_after": exim_stage_2.ignore_bounce_after,
                "timeout_frozen_after": exim_stage_2.timeout_frozen_after,
                "global_maxmsgsize": exim_stage_2.global_msg_max_size,
                "max_received": exim_stage_2.received_headers_max,
                "received_header_text": exim_stage_2.header_txt,
            })

    def dump_exim_stage_4(self) -> None:
        """
        Dump exim_stage4 configuration file.
        """
        disable_ipv6 = True
        antispam = AntiSpam.first()

        if exim_stage_4.use_incoming_tls:
            http_server = "https://{}/rs.php".format(httdp_config.servername)
        else:
            http_server = "http://{}/rs.php".format(httdp_config.servername)

        for interface in network.get_interfaces():
            if not network.is_ipv6_disabled(interface):
                disable_ipv6 = False
                break

        outscript = "{}/scripts/exim/spam_route.pl".format(
            self._mc_config.get_value("SRCDIR"))
        optimized_script = "{}/scripts/exim/spam_route.opt.pl".format(
            self._mc_config.get_value("SRCDIR"))
        if os.path.isfile(optimized_script):
            outscript = optimized_script
        byte_compiled_script = "{}/scripts/exim/spam_route.bbin".format(
            self._mc_config.get_value("SRCDIR"))
        if os.path.isfile(byte_compiled_script):
            outscript = byte_compiled_script

        exim_stage_4 = MTAConfig.find_by_set_id_and_stage_id(set_id=1,
                                                             stage_id=4)
        self.dump_template(
            template_config_src_file='etc/exim/exim_stage4.conf_template',
            config_datas={
                "VARDIR":
                self._mc_config.get_value("VARDIR"),
                "SRCDIR":
                self._mc_config.get_value("SRCDIR"),
                "allow_mx_to_ip":
                exim_stage_4.allow_mx_to_ip,
                "archiver_host":
                self.system_conf.archiver_host.split(':')[0],
                "archiver_port":
                self.system_conf.archiver_host.split(':')[1],
                "db_passwd":
                self._mc_config.get_value("MYMAILCLEANERPWD"),
                "disable_ipv6":
                disable_ipv6,
                "errors_reply_to":
                exim_stage_4.errors_reply_to,
                "global_max_msg_size":
                exim_stage_4.global_msg_max_size,  # GLOBAL_MAXMSGSIZE
                "helo_name":
                get_helo_name(),
                "hosts_require_tls":
                exim_stage_4.hosts_require_tls.encode('utf-8').split('\r\n'),
                "max_rcpt":
                exim_stage_4.max_rcpt,
                "max_received":
                exim_stage_4.received_headers_max,
                "outscript":
                outscript,
                "report_url":
                http_server,
                "retry_rule":
                exim_stage_4.retry_rule,
                "smtp_banner":
                exim_stage_4.smtp_banner,
                "syslog_enabled":
                'syslog : ' if exim_stage_4.use_syslog else
                None,  # __IF_USE_SYSLOGENABLED__
                "tag_mode_bypass_whitelists":
                antispam.tag_mode_bypass_whitelist,
                "use_archiver":
                self.system_conf.use_archiver,  # USEARCHIVER
                "use_tls":
                exim_stage_4.use_incoming_tls,
                "use_syslog":
                "syslog_facility = local1\nsyslog_processname = stage1"
                if exim_stage_4.use_syslog else
                "#no syslog_facility",  # __IF_USE_SYSLOG__
            })
        pass

    def dump_spam_route(self):
        # TODO: finish the implementation
        names = DnsList().get_all_name()
        print()
