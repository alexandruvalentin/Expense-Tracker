from expense import Expense
import calendar
import datetime

import gspread
import csv
from google.oauth2.service_account import Credentials


def main():
    print("We're live!")
    expense_file_path = "expenses.csv"
    budget = 2000
    
    # Get user input for expense
    expense = get_user_expense()

    # Write their input to a file
    save_expense_to_file(expense, expense_file_path)

    # Read file and summarize expenses
    summarize_expense(expense_file_path, budget)

    # Upload Expense file to Google Sheets
    csv_to_sheets(expense_file_path)

def get_user_expense():
    print("Getting user expense")
    expense_name = input("Enter expense name:")
    expense_amount = float(input("Enter expense amount:"))
    print(f"You've entered {expense_name}, {expense_amount}€")

    expense_categories = [
        "🍔 Food",
        "🏠 Home",
        "💼 Work",
        "🎉 Fun",
        "✨ Misc"
    ]

    while True:
        print("Select a category: ")
        for i, category_name in enumerate(expense_categories):
            print(f" {i + 1}. {category_name} ")
        
        try:
            value_range = f"[1 - {len(expense_categories)}]"
            selected_index = int(input(f"Enter a category number {value_range}: ")) - 1
            if selected_index in range(len(expense_categories)):
                selected_category = expense_categories[selected_index]
                new_expense = Expense(name=expense_name, category=selected_category, amount=expense_amount)
                return new_expense
            else:
                print("Invalid Category. Please try again!")
        except Exception as e:
            print("Invalid input, please try again!")

        

def save_expense_to_file(expense: Expense, expense_file_path):
    print(f"Saving user expense: {expense} to {expense_file_path}")
    with open(expense_file_path, "a", encoding="utf-8") as f:
        f.write(f"{expense.name}, {expense.amount}, {expense.category}\n")



def summarize_expense(expense_file_path, budget):
    print("Summarizing user expense")
    expenses: list[Expense] = []
    with open(expense_file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            expense_name, expense_amount, expense_category = line.strip().split(",")
            line_expense = Expense(name=expense_name, amount=float(expense_amount), category=expense_category)
            expenses.append(line_expense)

    amount_by_category = {}
    for expense in expenses:
        key = expense.category
        if key in amount_by_category:
            amount_by_category[key] += expense.amount
        else:
            amount_by_category[key] = expense.amount

    print("Expenses by Category 📊")
    for key, amount in amount_by_category.items():
        print(f"  {key}: €{amount:.2f}")

    total_spent = sum([x.amount for x in expenses])
    print(f"💶 Total spent: €{total_spent:.2f}")

    remaining_budget = budget - total_spent
    print(f"✅ Remaining budget: €{remaining_budget:.2f}.")

    # Get the current date
    now = datetime.datetime.now()

    # Get the number of days in the current month
    days_in_month = calendar.monthrange(now.year, now.month)[1]

    # Calculate the remaining number of days in the current month
    remaining_days = days_in_month - now.day
    print(f"Remaining number of days in the current month: {remaining_days}")

    daily_budget = remaining_budget / remaining_days
    print(f"👉 Budget per day: €{daily_budget:.2f}")


def csv_to_sheets(expense_file_path):
    scopes = ['https://www.googleapis.com/auth/spreadsheets']
    credentials = Credentials.from_service_account_file("credentials.json", scopes=scopes)
    client = gspread.authorize(credentials)

    workbood_id = "1OiUaisVRa6n0Z9Mgr7ZwMFOR2wHmdpeTlMt8wraQ8uQ"
    workbook = client.open_by_key(workbood_id)

    sheet = workbook.worksheet("SecondSheet")
    sheet.clear()

    f = open(expense_file_path, "r", encoding='utf-8')
    values = [r for r in csv.reader(f)]

    sheet.update(f"A1:C{len(values)}", values)
    

if __name__ == "__main__":
    main()