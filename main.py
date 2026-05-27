import datetime  
import csv

FILENAME = "transactions.csv" 
FIELDNAMES = ["date", "transaction_type", "category", "amount", "description"]

class Transaction:
    def __init__(self, date: str, transaction_type: str, category: str, amount: float, description: str):
            self.date = date
            self.transaction_type = transaction_type
            self.category = category
            self.amount = amount
            self.description = description
    
    def to_dict(self) -> dict[str, str | float]:
        return {
            "date": self.date,
            "transaction_type": self.transaction_type,
            "category": self.category,
            "amount": self.amount,
            "description": self.description
        }


class Tracker:
    def __init__(self):
        self.transactions: list[Transaction] = []

    def add_transaction(self, transaction: Transaction):
        self.transactions.append(transaction)
    
    def save_transaction(self,transaction:Transaction):
        with open(FILENAME, "a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=FIELDNAMES )
            
            if file.tell() == 0:
                writer.writeheader()
            writer.writerow(transaction.to_dict())

            print("Transaction saved to CSV")

    def load_transactions(self):
        try:
            with open(FILENAME, "r", newline="") as file:
                reader = csv.DictReader(file)

                for row in reader:
                    transaction = Transaction(
                        row["date"],
                        row["transaction_type"],
                        row["category"],
                        float(row["amount"]),
                        row["description"]
                    )
                    self.add_transaction(transaction)

        except FileNotFoundError:
            print("No existing transactions found. Starting with an empty list.")

    def get_monthly_summary(self,month: str):
        total_income=0
        total_expense=0

        for transaction in self.transactions:
            if transaction.date.startswith(month):
                if transaction.transaction_type == "income":
                    total_income += transaction.amount
                elif transaction.transaction_type == "expense":
                    total_expense += transaction.amount
        
        balance = total_income - total_expense
        return total_income, total_expense, balance
    
    def filter_by_category(self, category: str):
        matches: list[Transaction] = []

        for transaction in self.transactions:
            if transaction.category.lower() == category.lower():
                matches.append(transaction)

        return matches
    
    def filter_by_date_range(
        self,
        start_date: datetime.datetime,
        end_date: datetime.datetime
    ) -> list[Transaction]:
        matches: list[Transaction] = []

        for transaction in self.transactions:
            transaction_date = datetime.datetime.strptime(transaction.date, "%Y-%m-%d")

            if start_date <= transaction_date <= end_date:
                matches.append(transaction)

        return matches
    
    def export_monthly_report(self, month: str):
        report_filename = f"report_{month}.csv"
        found = False

        with open(report_filename, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
            writer.writeheader()

            for transaction in self.transactions:
                if transaction.date.startswith(month):
                    writer.writerow(transaction.to_dict())
                    found = True

        return found, report_filename

def print_transactions(transactions: list[Transaction]):
    if len(transactions) == 0:
        print("No transactions found")
    else:
        print("{:<5} {:<12} {:<12} {:<15} {:>10} {:<20}".format(
            "No", "Date", "Type", "Category", "Amount", "Description"
        ))

        for i, transaction in enumerate(transactions, start=1):
            print(
                f"{i:<5} "
                f"{transaction.date:<12} "
                f"{transaction.transaction_type:<12} "
                f"{transaction.category:<15} "
                f"{transaction.amount:>10.2f} "
                f"{transaction.description:<20}"
            )


tracker = Tracker()
tracker.load_transactions()

while True:
    print("\nEXPENSE TRACKER")
    print("1.Add expenses/Income")
    print("2. Show expenses")
    print("3. Exit")
    print("4. Summary")
    print("5. Filter by category")
    print("6. Filter by date")
    print("7. Export Monthly report")


    
    option = input("Enter your option(1/2/3/4/5/6/7): ")

    if option == "1" :
        print("\nADD INCOME/EXPENSES")

        transaction_type = input("Enter type (income/expense): ").strip().lower()
        if transaction_type not in ["income","expense"]:
            print("invalid type")
            continue

        date = input("Enter date (YYYY-MM-DD):")
        try:
            date_object = datetime.datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            print("invalid data format")
            continue


        category = input("Enter category :").strip().lower()

        try:
            amount = float(input("Enter amount: "))
        except ValueError:
            print("invalid amount")
            continue
        if amount <= 0:
            print("amount must be greater than 0")
            continue
        
        description = input("Enter description: ")

        expense = Transaction(
            date_object.strftime("%Y-%m-%d"),
            transaction_type,
            category,
            amount,
            description
        )
        tracker.add_transaction(expense)
        tracker.save_transaction(expense)
        print("Expense added successfully")
        
    elif option == "2":
        print("\nAll transactions")
        print_transactions(tracker.transactions)

    elif option == "3":
        print("Exiting...")
        break
    elif option == "4":
        print("MONTHLY SUMMARY")
        month = input("Enter month(YYYY-MM): ")
        try:
            month_object = datetime.datetime.strptime(month, "%Y-%m")
        except ValueError:
            print("invalid month format")
            continue
        
        total_income, total_expense, balance = tracker.get_monthly_summary(month)
        print("Month -", month)
        print(f"TOTAL INCOME: {total_income:.2f}")
        print(f"TOTAL EXPENSES: {total_expense:.2f}")
        print(f"Balance: {balance:.2f}")


    elif option == "5":
        print("Filter By Category")
        filter_cat = input("Enter Category: ").strip().lower()

        matches = tracker.filter_by_category(filter_cat)
        print_transactions(matches)
    
    elif option == "6":
        start_date = input("enter start date:")
        try:
            start_object = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        except ValueError:
            print("invalid date format")
            continue

        end_date = input("enter end date: ")
        try:
            end_object = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError:
            print("invalid date format")
            continue
        
        if start_object > end_object: 
            print("invalid date range")
            continue

        
        matches = tracker.filter_by_date_range(start_object, end_object)
        print_transactions(matches)

  
    elif option == "7":
        print("Export monthly report to CSV")

        month = input("Enter month(YYYY-MM): ")
        try:
            month_object = datetime.datetime.strptime(month, "%Y-%m")
        except ValueError:
            print("invalid month format")
            continue

        found, report_filename = tracker.export_monthly_report(month)

        if found:
            print("Report exported:", report_filename)
        else:
            print("No transaction found for this month")
       
    else:
        print("wrong input")