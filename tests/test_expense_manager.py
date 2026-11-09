import tempfile
import unittest
from pathlib import Path

from expense_manager import ExpenseManager


class ExpenseManagerTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        database_path = str(Path(self.temp_dir.name) / "test_pennylog.db")
        self.manager = ExpenseManager(database_path)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_add_and_list_expense(self):
        expense_id = self.manager.add_expense(
            125.50, "Food", "Lunch", "2026-11-09"
        )
        expenses = self.manager.get_all_expenses()

        self.assertEqual(len(expenses), 1)
        self.assertEqual(expenses[0]["id"], expense_id)
        self.assertEqual(expenses[0]["category"], "Food")
        self.assertAlmostEqual(expenses[0]["amount"], 125.50)

    def test_reject_invalid_expense(self):
        with self.assertRaises(ValueError):
            self.manager.add_expense(-10, "Food")

        with self.assertRaises(ValueError):
            self.manager.add_expense(10, " ")

    def test_delete_expense(self):
        expense_id = self.manager.add_expense(50, "Travel")

        self.assertTrue(self.manager.delete_expense(expense_id))
        self.assertFalse(self.manager.delete_expense(expense_id))
        self.assertEqual(self.manager.get_all_expenses(), [])

    def test_monthly_total(self):
        self.manager.add_expense(100, "Food", expense_date="2026-11-02")
        self.manager.add_expense(200, "Travel", expense_date="2026-11-08")
        self.manager.add_expense(500, "Books", expense_date="2026-10-30")

        self.assertAlmostEqual(self.manager.get_monthly_total("2026-11"), 300)

    def test_budget_and_summary(self):
        self.manager.add_expense(250, "Food", expense_date="2026-11-03")
        self.manager.set_monthly_budget(1000, "2026-11")

        summary = self.manager.get_monthly_summary("2026-11")
        self.assertAlmostEqual(summary["spent"], 250)
        self.assertAlmostEqual(summary["budget"], 1000)
        self.assertAlmostEqual(summary["remaining"], 750)
        self.assertFalse(summary["over_budget"])

    def test_over_budget(self):
        self.manager.add_expense(1200, "Shopping", expense_date="2026-11-03")
        self.manager.set_monthly_budget(1000, "2026-11")

        summary = self.manager.get_monthly_summary("2026-11")
        self.assertTrue(summary["over_budget"])
        self.assertAlmostEqual(summary["remaining"], -200)


if __name__ == "__main__":
    unittest.main()
