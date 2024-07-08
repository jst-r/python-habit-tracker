import click
import peewee

from analytics import (
    get_habit_names,
    longest_streak_all,
    find_longest_streak,
    make_period_selector,
    select_all,
)
import data_model
from data_model import Habit
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
@click.option(
    "--period",
    "-p",
    type=PERIOD_CHOICE,
    help="Only list habits with this period",
)
def list(period: str | None):
    if period is None:
        selector = select_all
    else:
        selector = make_period_selector(PERIOD_FROM_OPTION[period])

    names = get_habit_names(selector)

    click.echo("Here is the list of habits:")
    for name in names:
        click.echo("\t" + name)


@cli.command()
@click.option("--name", "-n", type=str)
def streak(name: str | None):
    """
    Find the longest streak.
    If no name name is provided, searches across all habits.
    If a name is provided, returns the longest streak for that habit.
    """
    if name is not None:
        habit = Habit.get(Habit.name == name)

        length = find_longest_streak(habit)
        click.echo(
            f"Longest streak for the habit '{name}' is {length} days. Great job!"
        )
    else:
        habit, length = longest_streak_all()
        click.echo(
            f"Habit with the longest streak is '{habit.name}' at {length} days in a row. Great job!"
        )
