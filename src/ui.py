import click
import peewee

from data_model import insert_example_data
from period import Period
from tracking import new_habit

PERIOD_OPTIONS = ["daily", "d", "weekly", "w"]
PERIOD_CHOICE = click.Choice(PERIOD_OPTIONS, case_sensitive=False)
PERIOD_FROM_OPTION = {
    "daily": Period.DAILY,
    "d": Period.DAILY,
    "weekly": Period.WEEKLY,
    "w": Period.WEEKLY,
}


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
    type=PERIOD_CHOICE,
    required=True,
    help="How often do you plan to complete this habit",
)
def add(name: str, period: str):
    """
    Create a new habit with the provided name and period.

    Example: add "Do the dishes" -p d
    """
    try:
        new_habit(name, PERIOD_FROM_OPTION[period])
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
