import datetime  

expenses: list[dict] = []

while True:
    print("\nEXPENSE TRACKER")
    print("1.Add expenses/Income")
    print("2. Show expenses")
    print("3. Exit")
    print("4. Summary")
    print("5. Filter by category")
    
    option = input("Enter your option(1/2/3/4/5): ")

    if option == "1" :
        print("\nADD INCOME/EXPENSES")

        type = input("Enter type (income/expense): ").lower()
        if type not in ["income","expense"]:
            print("invalid type")
            continue

        date = input("Enter date (YYYY-MM-DD):")
        try:
            date_object = datetime.datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            print("invalid data format")
            continue


        category = input("Enter category :")

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
            "date": date,
            "type": type,
            "category": category,
            "amount": amount,
            "description": description
        }
        expenses.append(expense)

        print("Expense added successfully")
        
    elif option == "2":
        print("\nTotal expenses")
        if len(expenses)==0:
            print("No expense added")
        else:
            print("{:<5} {:<12} {:<12} {:<15} {:>10} {:<20}".format("No", "Date", "Type", "Category", "Amount", "Description"))

            for i,expense in enumerate(expenses, start=1):
                print(f"{i:<5} {expense['date']:<12} {expense['type']:<12} {expense['category']:<15} {expense['amount']:>10.2f} {expense['description']:<20}")

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

        for expense in expenses:
            if expense["date"].startswith(month):
                if expense["type"] == "income":
                    total_income += expense["amount"]
                elif expense["type"] == "expense":
                    total_expense += expense["amount"]

        
        print("Month - ",month)
        print("TOTAL INCOME",total_income)
        print("TOTAL EXPENSES",total_expense)
        print("Balance =",total_income-total_expense)

    elif option == "5":
        print("Filter By Category")
        filter_cat = input("Enter Category: ").strip().lower()

        found = False
        for expense in expenses:
            if expense["category"].lower() ==filter_cat:
                print((f" {expense['date']:<12} {expense['type']:<12} {expense['category']:<15} {expense['amount']:>10.2f} {expense['description']:<20}"))
                found = True
        if not found:
            print("No expenses found for the category:", filter_cat)

    else:
        print("wrong input")