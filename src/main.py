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


db.connect()
db.create_tables([Habit, Completion])

db.close()
