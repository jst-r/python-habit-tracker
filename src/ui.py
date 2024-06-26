import click


@click.group()
def cli():
    pass


@cli.command(help="Add example data to the tracker")
def init():
    pass


@cli.command()
def add():
    pass


@cli.command()
def remove():
    pass


@cli.command()
def list():
    pass


@cli.command()
def streak():
    pass
