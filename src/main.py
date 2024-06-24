from analytics import get_completion_dates, split_streaks
from data_model import Completion, Habit, db
from period import Period


db.connect()
db.create_tables([Habit, Completion])


dates = get_completion_dates(Habit.get(Habit.name == "Clean the house"))
streaks = split_streaks(sorted(dates), Period.WEEKLY)

print(*sorted(dates), sep="\n")
print("=" * 20)
print("=" * 20)

for s in streaks:
    print(*s, sep="\n")
    print("=" * 20)

db.close()
