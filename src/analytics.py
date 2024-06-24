from datetime import datetime
from data_model import Habit
from period import PERIOD_META, Period


def get_all_habit_names():
    return [habit.name for habit in Habit.select()]


def get_all_habits_by_period(period: Period):
    return [habit.name for habit in Habit.select().where(Habit.period == period)]


def get_completion_dates(habit: Habit):
    return [completion.date for completion in habit.completions]


def split_streaks(dates: list[datetime], period: Period) -> list[list[datetime]]:
    dt = PERIOD_META[period].length
    get_start = PERIOD_META[period].get_period_start

    streaks = []
    curr_streak = [dates[0]]
    streak_start = get_start(dates[0])

    for t in dates[1:]:
        if t < streak_start + len(curr_streak) * dt:
            # habit was marked multiple times in a single period
            continue
        elif t < streak_start + (len(curr_streak) + 1) * dt:
            # streak continues
            curr_streak.append(t)
        else:
            # streak was broken
            streaks.append(curr_streak)
            curr_streak = [t]
            streak_start = get_start(t)

    streaks.append(curr_streak)

    return streaks


def max_streak(streaks: list[list[datetime]]):
    return max(map(len, streaks))
