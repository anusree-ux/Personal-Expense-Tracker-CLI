import datetime  

expenses: list[dict] = []

while True:
    print("\nEXPENSE TRACKER")
    print("1.Add expenses/Income")
    print("2. Show expenses")
    print("3. Exit")
    
    option = input("Enter your option(1/2/3): ")

    if option == "1" :
        print("\nAdd expenses")

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
            print("{:<5} {:<12} {:<15} {:>10} {:<20}".format("No", "Date", "Category", "Amount", "Description"))

            for i,expense in enumerate(expenses, start=1):
                print(f"{i:<5} {expense['date']:<12} {expense['category']:<15} {expense['amount']:>10.2f} {expense['description']:<20}")

    elif option == "3":
        print("Exiting...")
        break
    else:
        print("wrong input")