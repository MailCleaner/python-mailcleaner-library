import click
from click_default_group import DefaultGroup

from mailcleaner.dumper import DumpMySQLConfig

mysql_dump = DumpMySQLConfig()


@click.group(cls=DefaultGroup, default='all', default_if_no_args=True)
def cli():
    """Dump mysql configuration files."""
    pass


@click.command()
def all():
    """Dump configurations of all mysql instances (master and slave)."""
    mysql_dump.dump()


@click.command()
def master():
    """Dump configurations of mysql master instance."""
    mysql_dump.dump_master_config()


@click.command()
def slave():
    """Dump configurations of mysql slave instance."""
    mysql_dump.dump_slave_config()


cli.add_command(all)
cli.add_command(master)
cli.add_command(slave)

if __name__ == '__main__':
    cli()
