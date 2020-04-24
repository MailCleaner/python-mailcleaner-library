import click
from mailcleaner.dumper import DumpFail2banConfig
from click_default_group import DefaultGroup

fail2ban_dump = DumpFail2banConfig()


@click.group(cls=DefaultGroup, default='all', default_if_no_args=True)
def cli():
    """Dump fail2ban configuration jails."""
    pass


@click.command()
def all():
    """Dump configurations of all mysql instances (master and slave)."""
    fail2ban_dump.dump()


@click.command()
def exim():
    """Dump jail configuration for exim."""
    fail2ban_dump.dump_exim_jail_conf()


@click.command()
def ssh():
    """Dump jail configuration for ssh."""
    fail2ban_dump.dump_ssh_jail_conf()


@click.command()
def webauth():
    """Dump jail configuration for webauth."""
    fail2ban_dump.dump_webauth_jail_conf()


cli.add_command(all)
cli.add_command(exim)
cli.add_command(ssh)
cli.add_command(webauth)

if __name__ == '__main__':
    cli()
