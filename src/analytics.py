from datetime import datetime
from typing import Callable
from data_model import Habit
from period import PERIOD_META, Period

type Selector = Callable[[], list[Habit]]


def select_all() -> list[Habit]:
    return list(Habit.select())


def make_period_selector(period: Period) -> Selector:
    def selector():
        return list(Habit.select().where(Habit.period == period))

    return selector


def get_habit_names(selector: Selector) -> list[str]:
    return [str(habit.name) for habit in selector()]


def longest_streak_all(name: str) -> tuple[str, int]:
    max_len = 0
    max_name = "NO HABITS"
    for habit in Habit.select():
        dates = get_completion_dates(habit)
        streaks = split_streaks(dates, habit.period)
        l = max_streak_len(streaks)
        if l > max_len:
            max_len = l
            max_name = habit.name

    return (max_name, max_len)


def longest_streak_by_name(name: str) -> int:
    habit = Habit.get(Habit.name == name)
    dates = get_completion_dates(habit)
    streaks = split_streaks(dates, habit.period)
    return max_streak_len(streaks)


def get_completion_dates(habit: Habit) -> list[datetime]:
    return [completion.date for completion in habit.completions]  # type: ignore


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


def max_streak_len(streaks: list[list[datetime]]) -> int:
    return max(map(len, streaks))
