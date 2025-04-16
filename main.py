from bank_account import BankAccount

user_id = input("Enter your user ID: ")
account = BankAccount(user_id)
account.create_account()

while True:
    print("\nChoose an option:")
    print("1. Check Balance")
    print("2. Deposit")
    print("3. Withdraw")
    print("4. Exit")

    choice = input("Enter your choice (1–4): ")

    if choice == '1':
        # Call get_balance() once you've implemented it
        pass
    elif choice == '2':
        # Prompt for amount and call deposit()
        pass
    elif choice == '3':
        # Prompt for amount and call withdraw()
        pass
    elif choice == '4':
        print("Goodbye!")
        break
    else:
        print("Invalid choice. Try again.")