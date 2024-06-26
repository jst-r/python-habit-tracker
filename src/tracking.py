from data_model import Completion, Habit
from period import Period


def new_habit(name: str, period: Period):
    habit = Habit(name=name, period=period)
    habit.save()


def delete_habit(name: str):
    habit = Habit.get(Habit.name == name)
    habit.delete_instance(recursive=True)  # Also delete related completions


def mark_completed(name: str):
    habit = Habit.get(Habit.name == name)
    completion = Completion(habit=habit)
    completion.save()
