from data_model import Completion, Habit, db
from ui import cli


def main():
    db.connect()
    db.create_tables([Habit, Completion])

    cli()

    db.close()


if __name__ == "__main__":
    main()
