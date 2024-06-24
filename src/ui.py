import click


@click.group()
def cli():
    pass


@cli.command(help="Add example data to the tracker")
def init():
    pass
