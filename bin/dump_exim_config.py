import click
from click_default_group import DefaultGroup

from mailcleaner.dumper import DumpEximConfig

exim_dump = DumpEximConfig()


@click.group(cls=DefaultGroup, default='all', default_if_no_args=True)
def cli():
    """Dump exim configuration stages."""
    pass


@click.command()
def all():
    """Dump configurations of all exim stages."""
    exim_dump.dump()


@click.command()
def stage_1():
    """Dump configurations of exim stage 1."""
    exim_dump.dump_exim_stage_1()


@click.command()
def stage_2():
    """Dump configurations of exim stage 2."""
    exim_dump.dump_exim_stage_2()


@click.command()
def stage_4():
    """Dump configurations of exim stage 4."""
    exim_dump.dump_exim_stage_4()


cli.add_command(all)
cli.add_command(stage_1)
cli.add_command(stage_2)
cli.add_command(stage_4)

if __name__ == '__main__':
    cli()
