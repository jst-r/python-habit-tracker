# Habit
Habit is a minimal habit tracker CLI app I wrote for an assigment at the International University of Applied Sciences.

It is written in Python and uses SQLite3 with Peewee ORM for data storage.

## Installation

Habit is developed using Python 3.12, however any reasonably modern version should work fine.

```bash
# Clone the source code
git clone https://github.com/jst-r/python-habit-tracker.git
# Move to the project directory
cd python-habit-tracker
# (optional) Initialize a virutal enviroment. Omit this step if you want to perform system wide installation. 
py -m venv virtual_enviroment
# Install the project
pip install .
# Verify installation
habit --help
```

Note: `py` is the python executable on Windows. If you use a different OS, substitute `py` with `python3`.

## Usage
```bash
# See all available commands
habit --help
# Documentation on a specific command
habit command --help
# E.g.
habit add --help

# Populate the dabase with example habits and completions
habit init

# List habits
habit list
# List daily habits
habit list --period daily
# Or
habit list -p d

# Create new habit
habit add -p w "Somehting I need to do every week"

# Mark a habit that you have completed today
habit mark "Somehting I need to do every week"

# Delete a habit and its completions
habit delete "Somehting I need to do every week"

# Find a habit with the longest streak
habit streak
```

Streaks for habits with different periods are compared base on total amount of days. E.g. 2 weeks is converted to 14 days, which means that a streak of 2 weeks will be reported as longer than a streak of 13 daily completions.

## Testing
First, follow the installation steps.
```bash
# Install test requirements
pip install -r tests/requirements.txt
# Run the tests
pytest
```

Refer to pytest documentation for more information on running tests.

Database path is set to in-memory during in tests in order to speed up test execution and prevent flaky test. Implemented in `tests/__init__.py`.

## Data storage
By default, data is stored as a sqlite database in the `~/.python_tracker_directory` directory. I.e. a folder in the user directory.

To avoid polluting your disk, you can set the `PYTHON_HABIT_TRACKER_DB_PATH` enviroment variable to a file name (e.g. `db`). Which will create the dabase file in the project directory root.