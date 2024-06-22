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
    start_time = datetime.now() - timedelta(days=7 * 5)

    for name in ["Exercise", "Brush teeth", "Drink 2 liters of water"]:
        habit = Habit(name=name, period=Period.DAILY)
        habit.save()

        for delta in range(7 * 4):
            if random.random() > COMPLETION_RATE:
                print("skipped")
                continue
            completion = Completion(
                habit=habit, date=start_time + timedelta(days=delta)
            )
            completion.save()

    for name in ["Clean the house", "Call mom"]:
        habit = Habit.create(name=name, period=Period.WEEKLY)
        habit.save()

        for delta in range(0, 7 * 4, 7):
            if random.random() > COMPLETION_RATE:
                continue
            completion = Completion(date=start_time + timedelta(days=delta))
            completion.habit = habit
            completion.save()


def get_all_habit_names():
    return [habit.name for habit in Habit.select()]


def get_all_habits_by_period(period: Period):
    return [habit.name for habit in Habit.select().where(Habit.period == period)]


def get_completion_dates(habit: Habit):
    return [completion.date for completion in habit.completions]


def zero_time(dt: datetime):
    return datetime(dt.year, dt.month, dt.day)


def get_streaks(dates: list[datetime]) -> list[list[datetime]]:
    streaks = []
    curr_streak = []
    for a, b in zip(dates, dates[1:]):
        curr_streak.append(a)
        a, b = zero_time(a), zero_time(b)
        if a != b - timedelta(days=1):
            streaks.append(curr_streak)
            curr_streak = []

    curr_streak.append(dates[-1])
    streaks.append(curr_streak)

    return streaks


def max_streak(streaks: list[list[datetime]]):
    return max(map(len, streaks))


db.connect()
db.create_tables([Habit, Completion])

dates = get_completion_dates(Habit.get(Habit.name == "Exercise"))
streaks = get_streaks(sorted(dates))

print(*sorted(dates), sep="\n")
print("=" * 20)
print("=" * 20)

for s in streaks:
    print(*s, sep="\n")
    print("=" * 20)

db.close()
