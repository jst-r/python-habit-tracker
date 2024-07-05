from typing import Callable

from enum import IntEnum
from datetime import datetime, timedelta
from dataclasses import dataclass


@dataclass
class PeriodMetadata:
    length: timedelta
    get_period_start: Callable[[datetime], datetime]
    unit: str


class Period(IntEnum):
    DAILY = 1
    WEEKLY = 2

    @property
    def meta(self) -> PeriodMetadata:
        return __PERIOD_META[self]


def zero_time(dt: datetime):
    return datetime(dt.year, dt.month, dt.day)


def last_monday(dt):
    days_since_monday = dt.weekday()  # Monday is 0, Sunday is 6
    return dt - timedelta(days=days_since_monday)


__PERIOD_META = {
    Period.DAILY: PeriodMetadata(
        length=timedelta(days=1), get_period_start=zero_time, unit="days"
    ),
    Period.WEEKLY: PeriodMetadata(
        length=timedelta(days=7), get_period_start=last_monday, unit="weeks"
    ),
}
