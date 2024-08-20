from datetime import datetime
from typing import Callable
from data_model import Habit
from period import Period

# A closure or function that takes no arguments and returns a list of habits.
# Used to get analytics from an arbitrary selection of Habits.
type HabitSelector = Callable[[], list[Habit]]


def select_all() -> list[Habit]:
    return list(Habit.select())


def make_period_selector(period: Period) -> HabitSelector:
    def selector() -> list[Habit]:
        return list(Habit.select().where(Habit.period == period))

    return selector


def get_habit_names(selector: HabitSelector) -> list[str]:
    return [str(habit.name) for habit in selector()]


def longest_streak_all() -> tuple[Habit, int]:
    max_len = 0
    max_habit = None
    for habit in Habit.select():
        lenght = find_longest_streak(habit) * Period(habit.period).meta.length.days
        if lenght > max_len:
            max_len = lenght
            max_habit = habit

    if max_habit is None:
        raise ValueError("No habits found, can't find the longest streak")

    return (max_habit, max_len)


def find_longest_streak(habit: Habit) -> int:
    timestamps = get_completion_timestamps(habit)
    streaks = split_streaks(timestamps, Period(habit.period))
    return max_streak_len(streaks)


def get_completion_timestamps(habit: Habit) -> list[datetime]:
    return [completion.timestamp for completion in habit.completions]  # type: ignore


def split_streaks(timestamps: list[datetime], period: Period) -> list[list[datetime]]:
    dt = period.meta.length
    get_start = period.meta.get_period_start

    streaks = []
    curr_streak = [timestamps[0]]
    streak_start = get_start(timestamps[0])

    for t in timestamps[1:]:
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
