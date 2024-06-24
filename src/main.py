from data_model import Completion, Habit, db
from ui import cli

if __name__ == "__main__":
    db.connect()
    db.create_tables([Habit, Completion])

    cli()

    db.close()
