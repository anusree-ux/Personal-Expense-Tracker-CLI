import datetime  
import csv

FILENAME = "transactions.csv" 
FIELDNAMES = ["date", "transaction_type", "category", "amount", "description"]
transactions: list[dict] = []

try:
    with open(FILENAME, "r", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            row["amount"] = float(row["amount"])
            transactions.append(row)

except FileNotFoundError:
    print("No existing transactions found. Starting with an empty list.")

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

        expense = {
            "date": date_object.strftime("%Y-%m-%d"),
            "transaction_type": transaction_type,
            "category": category,
            "amount": amount,
            "description": description
        }
        transactions.append(expense)

        with open(FILENAME, "a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=FIELDNAMES )
            
            if file.tell() == 0:
                writer.writeheader()
            writer.writerow(expense)

            print("Transaction saved to CSV")

        print("Expense added successfully")
        
    elif option == "2":
        print("\nTotal expenses")
        if len(transactions)==0:
            print("No expense added")
        else:
            print("{:<5} {:<12} {:<12} {:<15} {:>10} {:<20}".format("No", "Date", "Type", "Category", "Amount", "Description"))

            for i,expense in enumerate(transactions, start=1):
                print(f"{i:<5} {expense['date']:<12} {expense['transaction_type']:<12} {expense['category']:<15} {expense['amount']:>10.2f} {expense['description']:<20}")

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

        total_income=0
        total_expense=0

        for expense in transactions:
            if expense["date"].startswith(month):
                if expense["transaction_type"] == "income":
                    total_income += expense["amount"]
                elif expense["transaction_type"] == "expense":
                    total_expense += expense["amount"]

        
        print("Month - ",month)
        print("TOTAL INCOME",total_income)
        print("TOTAL EXPENSES",total_expense)
        print("Balance =",total_income-total_expense)

    elif option == "5":
        print("Filter By Category")
        filter_cat = input("Enter Category: ").strip().lower()

        found = False
        for expense in transactions:
            if expense["category"].lower() ==filter_cat:
                print((f" {expense['date']:<12} {expense['transaction_type']:<12} {expense['category']:<15} {expense['amount']:>10.2f} {expense['description']:<20}"))
                found = True
        if not found:
            print("No expenses found for the category:", filter_cat)
    
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

        found  =  False

        for expense in transactions:
            transaction_date = datetime.datetime.strptime(expense["date"], "%Y-%m-%d")
            

            if start_object <= transaction_date <= end_object:
                print((f" {expense['date']:<12} {expense['transaction_type']:<12} {expense['category']:<15} {expense['amount']:>10.2f} {expense['description']:<20}"))
                found = True

        if not found:
            print("No expense in this data range")
  
    elif option == "7":
        print("Export monthly report to CSV")

        month = input("Enter month(YYYY-MM): ")
        try:
            month_object = datetime.datetime.strptime(month, "%Y-%m")
        except ValueError:
            print("invalid month format")
            continue

        report_filename = "report_" + month + ".csv"

        with open(report_filename, "w", newline="") as file:
            writer  = csv.DictWriter(file,fieldnames=FIELDNAMES)

            writer.writeheader()

            found = False

            for expense in transactions:
                if expense["date"].startswith((month)):
                    writer.writerow(expense)
                    found = True
            if found :
                print("Report exported:", report_filename)
            else:
                print("No transaction founf for this month")


                  

    else:
        print("wrong input")