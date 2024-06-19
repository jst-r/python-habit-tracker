from peewee import (
    SqliteDatabase,
    Model,
    CharField,
    DateField,
    IntegerField,
    ForeignKeyField,
)
from enum import Enum

DATABASE = "tracker.db"

db = SqliteDatabase(DATABASE)


class BaseModel(Model):
    class Meta:
        database = db


class Period(Enum):
    DAILY = 1
    WEEKLY = 2


class Habit(BaseModel):
    name = CharField()
    created_at = DateField()
    period = IntegerField()


class Completion(BaseModel):
    habit = ForeignKeyField(Habit, backref="completions")
    date = DateField()
