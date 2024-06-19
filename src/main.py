from peewee import (
    SqliteDatabase,
    Model,
    CharField,
    DateTimeField,
    IntegerField,
    ForeignKeyField,
)
from enum import Enum

db = SqliteDatabase("tracker.db")


class Period(Enum):
    DAILY = 1
    WEEKLY = 2


class Habit(Model):
    name = CharField()
    created_at = DateTimeField()
    period = IntegerField()

    class Meta:
        database = db


class Completion(Model):
    habit = ForeignKeyField(Habit, backref="completions")
    completed_at = DateTimeField()

    class Meta:
        database = db
