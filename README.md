# PennyLog

PennyLog is a beginner-friendly command-line expense tracker written in Python. It uses SQLite to save expenses and monthly budgets locally, so your records remain available the next time you run the program.

## Features

- Add an expense with an amount, category, optional note, and date
- View all saved expenses
- Delete an expense by its ID
- View total spending for the current month
- Set or update a monthly budget
- Check how much of the monthly budget remains
- Store data locally using SQLite

## Requirements

- Python 3.9 or newer
- No third-party packages are required

## Run the project

Clone the repository and open its folder in Terminal.

```bash
python3 pennylog.py
```

The first run automatically creates a local SQLite database file named `pennylog.db`.

## Run the tests

```bash
python3 -m unittest discover -s tests -v
```

The tests use temporary databases and do not change your personal PennyLog data.

## Project structure

```text
pennylog-expense-tracker/
├── pennylog.py
├── expense_manager.py
├── database.py
├── requirements.txt
├── README.md
└── tests/
    └── test_expense_manager.py
```

## How the code is organised

- `pennylog.py` displays the menu and collects user input.
- `expense_manager.py` contains expense and budget operations.
- `database.py` creates SQLite tables and opens database connections.
- `tests/` contains automated tests for the main application features.

This is a local command-line learning project. It does not currently include user accounts, cloud sync, or a graphical interface.
