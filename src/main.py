from datetime import date
from peewee import (
    SqliteDatabase,
    Model,
    CharField,
    DateTimeField,
    IntegerField,
    ForeignKeyField,
)
from enum import IntEnum
import random
from datetime import datetime, timedelta

DATABASE = "tracker.db"

db = SqliteDatabase(DATABASE)


class BaseModel(Model):
    class Meta:
        database = db


class Period(IntEnum):
    DAILY = 1
    WEEKLY = 7


class Habit(BaseModel):
    name = CharField(unique=True)  # Name is constrained unique to avoid user confusion
    created_at = DateTimeField(default=date.today)
    period = IntegerField()


class Completion(BaseModel):
    habit = ForeignKeyField(Habit, backref="completions")
    date = DateTimeField()


def insert_example_data():
    RANDOM_SEED = 42
    COMPLETION_RATE = 0.8

    random.seed(RANDOM_SEED)
    start_time = datetime.now()

    for name in ["Exercise", "Brush teeth", "Drink 2 liters of water"]:
        habit = Habit(name=name, period=Period.DAILY)
        habit.save()

        for delta in range(7 * 4):
            if random.random() > COMPLETION_RATE:
                print("skipped")
                continue
            completion = Completion(
                habit=habit, date=start_time - timedelta(days=delta)
            )
            completion.save()

    for name in ["Clean the house", "Call mom"]:
        habit = Habit.create(name=name, period=Period.WEEKLY)
        habit.save()

        for delta in range(0, 7 * 4, 7):
            if random.random() > COMPLETION_RATE:
                continue
            completion = Completion(date=start_time - timedelta(days=delta))
            completion.habit = habit
            completion.save()


db.connect()
db.create_tables([Habit, Completion])

insert_example_data()

db.close()
