from mailcleaner_db.models import Fail2banJail
from mailcleaner.dumper import DumpFail2banConfig


def test_dump_ssh_jail():
    ssh_jail_name = "mc-ssh"
    dump_fail2ban_config = DumpFail2banConfig()

    mc_jail = Fail2banJail.find_by_name(name=ssh_jail_name.replace('-', '_'))

    assert mc_jail is not None

    ssh_jail_configuration_content = dump_fail2ban_config.generate_config(
        template_config_src_file='etc/fail2ban/jail.d/{}.local_template'.
        format(ssh_jail_name),
        config_datas=vars(mc_jail))

    assert ssh_jail_configuration_content is not None
    assert ssh_jail_configuration_content is not ""
    assert str(mc_jail.enabled) in ssh_jail_configuration_content
    assert mc_jail.name in ssh_jail_configuration_content
    assert str(mc_jail.maxretry) in ssh_jail_configuration_content
    assert str(mc_jail.findtime) in ssh_jail_configuration_content
    assert str(mc_jail.bantime) in ssh_jail_configuration_content
    assert str(mc_jail.port) in ssh_jail_configuration_content
    assert mc_jail.filter in ssh_jail_configuration_content
    assert mc_jail.banaction in ssh_jail_configuration_content
    assert mc_jail.logpath in ssh_jail_configuration_content
