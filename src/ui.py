import click
import peewee

import data_model
from period import Period
from tracking import delete_habit, new_habit

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
    data_model.insert_example_data()


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
    except data_model.Habit.DoesNotExist:  # type: ignore ruff isn't smart enough to know it's there
        click.echo("A habit with this name already exists")


@cli.command()
@click.argument("name")
def delete(name: str):
    """Remove a habit with a given name and all corresponding completions"""
    try:
        delete_habit(name)
        click.echo(f"Deleted the habit '{name}' and all corresponding completions")
    except data_model.Habit.DoesNotExist:  # type: ignore ruff isn't smart enough to know it's there
        click.echo("Couldn't find a habit with this name")


@cli.command()
def list():
    pass


@cli.command()
def streak():
    pass
