from datetime import datetime, timedelta
from src.period import Period, zero_time, last_monday


def test_zero_time():
    assert zero_time(datetime(2024, 1, 1, 12, 1, 1)) == datetime(2024, 1, 1)
    assert zero_time(datetime(2024, 1, 1, 0, 0, 0)) == datetime(2024, 1, 1)
    assert zero_time(datetime(2024, 12, 31, 23, 59, 59)) == datetime(2024, 12, 31)
    assert zero_time(datetime(2024, 2, 29, 12, 0, 0)) == datetime(
        2024, 2, 29
    )  # Leap year


def test_last_monday():
    monday = datetime(2024, 1, 1)
    assert last_monday(datetime(2024, 1, 1)) == monday  # Monday
    assert last_monday(datetime(2024, 1, 2)) == monday  # Tuesday
    assert last_monday(datetime(2024, 1, 3)) == monday  # Wednesday
    assert last_monday(datetime(2024, 1, 4)) == monday  # Thursday
    assert last_monday(datetime(2024, 1, 5)) == monday  # Friday
    assert last_monday(datetime(2024, 1, 6)) == monday  # Saturday
    assert last_monday(datetime(2024, 1, 7, 23, 59, 59, 999)) == monday  # Sunday


def test_period_daily_meta():
    meta = Period.DAILY.meta
    assert meta.length == timedelta(days=1)
    assert meta.unit == "days"
    assert meta.get_period_start is zero_time


def test_period_weekly_meta():
    meta = Period.WEEKLY.meta
    assert meta.length == timedelta(days=7)
    assert meta.unit == "weeks"
    assert meta.get_period_start is last_monday
