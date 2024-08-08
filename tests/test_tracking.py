import pytest
import peewee

from period import Period
from data_model import db, Habit, Completion
from tracking import delete_habit, mark_completed, new_habit


@pytest.fixture(autouse=True)
def database_provider():
    db.connect()
    db.create_tables([Habit, Completion])

    yield

    db.close()


def test_new_habit():
    new_habit("a", Period.DAILY)
    assert len(Habit.select()) == 1
    new_habit("b", Period.WEEKLY)
    assert len(Habit.select()) == 2
    new_habit("c", Period.DAILY)
    assert len(Habit.select()) == 3

    assert sorted([h.name for h in Habit.select()]) == ["a", "b", "c"]


def test_unique_name():
    new_habit("a", Period.DAILY)

    with pytest.raises(peewee.IntegrityError):
        new_habit("a", Period.WEEKLY)


def test_mark():
    new_habit("a", Period.DAILY)
    new_habit("b", Period.DAILY)

    mark_completed("a")
    mark_completed("a")
    mark_completed("a")
    mark_completed("b")
    mark_completed("b")

    assert len(Completion.select()) == 5
    assert len(Habit.get(Habit.name == "a").completions) == 3
    assert len(Habit.get(Habit.name == "b").completions) == 2


def test_delete():
    new_habit("a", Period.DAILY)
    delete_habit("a")
    assert len(Habit.select()) == 0

    new_habit("a", Period.DAILY)
    mark_completed("a")
    mark_completed("a")
    delete_habit("a")
    assert len(Habit.select()) == 0
    assert len(Completion.select()) == 0
