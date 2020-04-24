import click
from click_default_group import DefaultGroup

from mailcleaner.dumper import DumpProxyConfig

proxy_dump = DumpProxyConfig()


@click.group(cls=DefaultGroup, default='dump', default_if_no_args=True)
def cli():
    """Dump ProxySql configuration file."""
    pass


@click.command()
def dump():
    """Dump configurations ProxySql."""
    proxy_dump.dump()


cli.add_command(dump)

if __name__ == '__main__':
    cli()
