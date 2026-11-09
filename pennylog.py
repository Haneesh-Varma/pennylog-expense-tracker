from datetime import date

from expense_manager import ExpenseManager


def show_menu():
    print("\n========== PENNYLOG ==========")
    print("1. Add expense")
    print("2. View all expenses")
    print("3. Delete an expense")
    print("4. View monthly summary")
    print("5. Set monthly budget")
    print("6. Exit")


def add_expense(manager):
    print("\n--- Add Expense ---")
    amount = input("Amount (₹): ")
    category = input("Category: ")
    note = input("Note (optional): ")
    date_text = input("Date (YYYY-MM-DD, leave blank for today): ").strip()

    try:
        expense_date = date.fromisoformat(date_text) if date_text else date.today()
        manager.add_expense(amount, category, note, expense_date)
        print("Expense saved successfully.")
    except ValueError as error:
        print(f"Could not add expense: {error}")


def view_expenses(manager):
    expenses = manager.get_all_expenses()

    if not expenses:
        print("\nNo expenses recorded yet.")
        return

    print("\nID | Date       | Category       | Amount (₹) | Note")
    print("-" * 72)

    for expense in expenses:
        print(
            f"{expense['id']:<2} | {expense['expense_date']} | "
            f"{expense['category']:<14} | {expense['amount']:>10.2f} | "
            f"{expense['note'] or '-'}"
        )


def delete_expense(manager):
    try:
        expense_id = int(input("Enter the expense ID to delete: "))

        if manager.delete_expense(expense_id):
            print("Expense deleted.")
        else:
            print("No expense found with that ID.")
    except ValueError:
        print("Please enter a valid numeric ID.")


def show_monthly_summary(manager):
    summary = manager.get_monthly_summary()

    print(f"\n--- Summary for {summary['month']} ---")
    print(f"Total spent: ₹{summary['spent']:.2f}")

    if summary["budget"] is None:
        print("No budget has been set for this month.")
    elif summary["over_budget"]:
        print(f"Monthly budget: ₹{summary['budget']:.2f}")
        print(f"You are over budget by ₹{abs(summary['remaining']):.2f}")
    else:
        print(f"Monthly budget: ₹{summary['budget']:.2f}")
        print(f"Budget remaining: ₹{summary['remaining']:.2f}")


def set_budget(manager):
    amount = input("Enter your monthly budget (₹): ")

    try:
        manager.set_monthly_budget(amount)
        print("Monthly budget saved.")
    except ValueError as error:
        print(f"Could not save budget: {error}")


def main():
    manager = ExpenseManager()

    while True:
        show_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_expense(manager)
        elif choice == "2":
            view_expenses(manager)
        elif choice == "3":
            delete_expense(manager)
        elif choice == "4":
            show_monthly_summary(manager)
        elif choice == "5":
            set_budget(manager)
        elif choice == "6":
            print("Your expenses are saved. See you next time.")
            break
        else:
            print("Please choose a number from 1 to 6.")


if __name__ == "__main__":
    main()
