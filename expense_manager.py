from datetime import date
import math

from database import get_connection, initialize_database


class ExpenseManager:
    """Contains the operations for expenses and monthly budgets."""

    def __init__(self, database_path="pennylog.db"):
        self.database_path = database_path
        initialize_database(self.database_path)

    def add_expense(self, amount, category, note="", expense_date=None):
        try:
            amount = float(amount)
        except (TypeError, ValueError):
            raise ValueError("Amount must be a valid number.")

        if not math.isfinite(amount) or amount <= 0:
            raise ValueError("Amount must be greater than zero.")

        category = category.strip()
        if not category:
            raise ValueError("Category cannot be empty.")

        if expense_date is None:
            expense_date = date.today()
        elif isinstance(expense_date, str):
            try:
                expense_date = date.fromisoformat(expense_date)
            except ValueError:
                raise ValueError("Date must use YYYY-MM-DD format.")

        if not isinstance(expense_date, date):
            raise ValueError("Please provide a valid date.")

        with get_connection(self.database_path) as connection:
            cursor = connection.execute(
                """
                INSERT INTO expenses (amount, category, note, expense_date)
                VALUES (?, ?, ?, ?)
                """,
                (amount, category, note.strip(), expense_date.isoformat()),
            )
            return cursor.lastrowid

    def get_all_expenses(self):
        with get_connection(self.database_path) as connection:
            rows = connection.execute(
                """
                SELECT id, amount, category, note, expense_date
                FROM expenses
                ORDER BY expense_date DESC, id DESC
                """
            ).fetchall()
        return [dict(row) for row in rows]

    def delete_expense(self, expense_id):
        with get_connection(self.database_path) as connection:
            cursor = connection.execute(
                "DELETE FROM expenses WHERE id = ?", (expense_id,)
            )
            return cursor.rowcount > 0

    def get_monthly_total(self, month=None):
        if month is None:
            month = date.today().strftime("%Y-%m")
        self._validate_month(month)

        with get_connection(self.database_path) as connection:
            row = connection.execute(
                """
                SELECT COALESCE(SUM(amount), 0) AS total
                FROM expenses
                WHERE expense_date >= ? AND expense_date < ?
                """,
                (f"{month}-01", self._next_month_start(month)),
            ).fetchone()
        return row["total"]

    def set_monthly_budget(self, amount, month=None):
        try:
            amount = float(amount)
        except (TypeError, ValueError):
            raise ValueError("Budget must be a valid number.")

        if not math.isfinite(amount) or amount <= 0:
            raise ValueError("Budget must be greater than zero.")

        if month is None:
            month = date.today().strftime("%Y-%m")
        self._validate_month(month)

        with get_connection(self.database_path) as connection:
            connection.execute(
                """
                INSERT INTO budgets (month, amount)
                VALUES (?, ?)
                ON CONFLICT(month) DO UPDATE SET amount = excluded.amount
                """,
                (month, amount),
            )

    def get_monthly_budget(self, month=None):
        if month is None:
            month = date.today().strftime("%Y-%m")
        self._validate_month(month)

        with get_connection(self.database_path) as connection:
            row = connection.execute(
                "SELECT amount FROM budgets WHERE month = ?", (month,)
            ).fetchone()
        return row["amount"] if row else None

    def get_monthly_summary(self, month=None):
        if month is None:
            month = date.today().strftime("%Y-%m")
        self._validate_month(month)

        spent = self.get_monthly_total(month)
        budget = self.get_monthly_budget(month)
        remaining = budget - spent if budget is not None else None

        return {
            "month": month,
            "spent": spent,
            "budget": budget,
            "remaining": remaining,
            "over_budget": budget is not None and spent > budget,
        }

    @staticmethod
    def _validate_month(month):
        try:
            date.fromisoformat(month + "-01")
        except (TypeError, ValueError):
            raise ValueError("Month must use YYYY-MM format.")

    @staticmethod
    def _next_month_start(month):
        ExpenseManager._validate_month(month)
        year, month_number = map(int, month.split("-"))
        if month_number == 12:
            return f"{year + 1:04d}-01-01"
        return f"{year:04d}-{month_number + 1:02d}-01"
