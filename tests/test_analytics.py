from datetime import datetime, timedelta
import pytest

from period import Period
from data_model import db, Habit, Completion, insert_example_data

from analytics import (
    find_longest_streak,
    longest_streak_all,
    select_all,
    make_period_selector,
    get_habit_names,
    split_streaks,
)


@pytest.fixture(autouse=True)
def database_provider():
    db.connect()
    db.create_tables([Habit, Completion])
    insert_example_data()

    yield

    db.close()


def test_get_names():
    assert get_habit_names(select_all) == [
        "Exercise",
        "Brush teeth",
        "Drink 2 liters of water",
        "Clean the house",
        "Call mom",
    ]
    assert get_habit_names(make_period_selector(Period.DAILY)) == [
        "Exercise",
        "Brush teeth",
        "Drink 2 liters of water",
    ]
    assert get_habit_names(make_period_selector(Period.WEEKLY)) == [
        "Clean the house",
        "Call mom",
    ]


def test_split_streaks_daily():
    t0 = datetime(2022, 2, 2)  # arbitrary
    day_offsets = [
        0,
        1,
        2,
        3.5,  # lands in the calendar day
        # missed
        5,
        6,
        7,
        # missed
        10,
        10.5,  # twice in a same day
        11,
        12,
        13,
        14,
        15,
    ]
    timestamps = [t0 + timedelta(days=offset) for offset in day_offsets]
    streaks = split_streaks(timestamps, Period.DAILY)

    assert len(streaks) == 3
    assert len(streaks[0]) == 4
    assert len(streaks[1]) == 3
    assert len(streaks[2]) == 6


def test_split_streaks_weekly():
    t0 = datetime(2002, 3, 19)  # arbitrary
    week_offsets = [
        0,
        1,
        2,
        3.5,  # still the same week
        # missed
        5,
        6,
        7,
        # missed
        10,
        10.5,  # twice a week
        11,
        12,
        13,
        14,
        15,
    ]
    timestamps = [t0 + timedelta(days=offset * 7) for offset in week_offsets]
    streaks = split_streaks(timestamps, Period.WEEKLY)

    assert len(streaks) == 3
    assert len(streaks[0]) == 4
    assert len(streaks[1]) == 3
    assert len(streaks[2]) == 6


def test_find_longest_streak():
    for name, streak_len in [
        ("Exercise", 11),
        ("Brush teeth", 14),
        ("Drink 2 liters of water", 6),
        ("Clean the house", 2),
        ("Call mom", 4),
    ]:
        assert find_longest_streak(Habit.get(Habit.name == name)) == streak_len


def test_find_longest_streak_all():
    for name, streak_len in [
        ("Call mom", 28),
        ("Brush teeth", 14),
        ("Clean the house", 14),
        ("Exercise", 11),
        ("Drink 2 liters of water", 6),
    ]:
        habit, got_len = longest_streak_all()
        assert name == habit.name
        assert streak_len == got_len

        habit.delete_instance(recursive=True)
