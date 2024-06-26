import click
import peewee

from data_model import insert_example_data
from period import Period
from tracking import new_habit


@click.group()
def cli():
    """
    For more detailed documentation try: command --help
    """
    pass


@cli.command()
def init():
    """
    Add example data to the tracker.
    """
    insert_example_data()


@cli.command()
@click.argument("name")
@click.option(
    "--period",
    "-p",
    type=click.Choice(["daily", "d", "weekly", "w"], case_sensitive=False),
    required=True,
    help="How often do you plan to complete this habit",
)
def add(name: str, period: Period):
    """
    Create a new habit with the provided name and period.

    Example: add "Do the dishes" -p d
    """
    try:
        new_habit(name, period)
    except peewee.IntegrityError:
        click.echo("A habit with this name already exists")


@cli.command()
def remove():
    pass


@cli.command()
def list():
    pass


@cli.command()
def streak():
    pass
