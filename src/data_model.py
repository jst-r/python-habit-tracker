from peewee import (
    SqliteDatabase,
    Model,
    CharField,
    DateTimeField,
    IntegerField,
    ForeignKeyField,
)
import random
from datetime import datetime, timedelta, date
import os

from period import Period


def get_db_path():
    """
    Gets the path to the database.
    By default a folder in the users home directory.
    Can be overwritten with the env variable `PYTHON_HABIT_TRACKER_DB_PATH`.
    It's a bit of a hacky but works fine.
    """
    if path := os.getenv("PYTHON_HABIT_TRACKER_DB_PATH"):
        return path

    user_data_dir = os.path.join(os.path.expanduser("~"), ".python_habit_tracker")
    os.makedirs(user_data_dir, exist_ok=True)
    return os.path.join(user_data_dir, "database.db")


DATABASE_PATH = get_db_path()
db = SqliteDatabase(DATABASE_PATH)


# Makes models a bit DRYer
class BaseModel(Model):
    class Meta:
        database = db


class Habit(BaseModel):
    # Name is constrained unique to avoid user confusion
    name = CharField(unique=True)
    created_at = DateTimeField(default=date.today)
    period = (
        IntegerField()
    )  # Should be created from Period type instead of providing raw integer


class Completion(BaseModel):
    habit = ForeignKeyField(Habit, backref="completions")
    timestamp = DateTimeField(default=date.today)


def insert_example_data():
    """
    Inserts example data into the database.
    Used for testing and providing example data for the user.
    Completions are inserted based on a seeded random value. Because of that the same set of completions is inserted every time the function is executed. This was done to avoid hard-coding many values.
    """
    RANDOM_SEED = 42
    COMPLETION_RATE = 0.8

    random.seed(RANDOM_SEED)
    start_time = datetime.now() - timedelta(days=7 * 5)

    for name in ["Exercise", "Brush teeth", "Drink 2 liters of water"]:
        habit = Habit(name=name, period=Period.DAILY)
        habit.save()

        for delta in range(7 * 4):
            # Random value mentioned in docsting
            if random.random() > COMPLETION_RATE:
                continue
            completion = Completion(
                habit=habit, timestamp=start_time + timedelta(days=delta)
            )
            completion.save()

    for name in ["Clean the house", "Call mom"]:
        habit = Habit.create(name=name, period=Period.WEEKLY)
        habit.save()

        for delta in range(0, 7 * 4, 7):
            # Random value mentioned in docsting
            if random.random() > COMPLETION_RATE:
                continue
            completion = Completion(timestamp=start_time + timedelta(days=delta))
            completion.habit = habit
            completion.save()
