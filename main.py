import sqlite3
import random
from datetime import datetime

#  Database Setup 
def create_database():
    conn = sqlite3.connect("banking.db")
    cursor = conn.cursor()

    # Accounts table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS accounts (
            account_number TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            pin TEXT NOT NULL,
            balance REAL DEFAULT 0.0
        )
    ''')

    # Transactions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_number TEXT,
            type TEXT,
            amount REAL,
            timestamp TEXT
        )
    ''')

    # Login attempts table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS login_attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_number TEXT,
            status TEXT,
            timestamp TEXT
        )
    ''')

    conn.commit()
    conn.close()

#  Account Class 
class Account:
    def __init__(self, account_number, name, pin, balance=0.0):
        self.account_number = account_number
        self.name = name
        self.pin = pin
        self.balance = balance

    def check_balance(self):
        return f"Your current balance is: ${self.balance:.2f}"

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            Bank.record_transaction(self.account_number, "Deposit", amount)
            return f"Deposited ${amount:.2f}. New balance: ${self.balance:.2f}"
        else:
            return "Deposit amount must be greater than 0."

    def withdraw(self, amount):
        if amount > 0 and amount <= self.balance:
            self.balance -= amount
            Bank.record_transaction(self.account_number, "Withdraw", amount)
            return f"Withdrew ${amount:.2f}. New balance: ${self.balance:.2f}"
        elif amount > self.balance:
            return "Insufficient funds!"
        else:
            return "Withdrawal amount must be greater than 0."

    def modify_account(self, new_name=None, new_pin=None):
        if new_name:
            self.name = new_name
        if new_pin:
            self.pin = new_pin
        return f"Account modified. New Name: {self.name}, New PIN: {self.pin}"

# --- Bank Class ---
class Bank:
    def __init__(self):
        create_database()

    def create_account(self, name, pin, balance=0.0):
        account_number = str(random.randint(100000, 999999))
        conn = sqlite3.connect("banking.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO accounts (account_number, name, pin, balance) VALUES (?, ?, ?, ?)",
                       (account_number, name, pin, balance))
        conn.commit()
        conn.close()
        return f"Account created successfully. Your account number is {account_number}"

    def close_account(self, account_number):
        conn = sqlite3.connect("banking.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM accounts WHERE account_number = ?", (account_number,))
        conn.commit()
        rows_deleted = cursor.rowcount
        conn.close()
        return "Account closed successfully." if rows_deleted else "Account not found."

    def authenticate(self, account_number, pin):
        conn = sqlite3.connect("banking.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM accounts WHERE account_number = ? AND pin = ?", (account_number, pin))
        result = cursor.fetchone()
        conn.close()

        # Log the attempt
        status = "Success" if result else "Failure"
        self.log_login_attempt(account_number, status)

        if result:
            return Account(*result)
        else:
            return None

    def update_account(self, account: Account):
        conn = sqlite3.connect("banking.db")
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE accounts
            SET name = ?, pin = ?, balance = ?
            WHERE account_number = ?
        ''', (account.name, account.pin, account.balance, account.account_number))
        conn.commit()
        conn.close()

    @staticmethod
    def record_transaction(account_number, type_, amount):
        conn = sqlite3.connect("banking.db")
        cursor = conn.cursor()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO transactions (account_number, type, amount, timestamp) VALUES (?, ?, ?, ?)",
                       (account_number, type_, amount, timestamp))
        conn.commit()
        conn.close()

    def log_login_attempt(self, account_number, status):
        conn = sqlite3.connect("banking.db")
        cursor = conn.cursor()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO login_attempts (account_number, status, timestamp) VALUES (?, ?, ?)",
                       (account_number, status, timestamp))
        conn.commit()
        conn.close()

# Main System 
def bank_system():
    bank = Bank()
    print("Welcome to the Online Banking System!")
    
    while True:
        print("\n1. Create Account")
        print("2. Log in")
        print("3. Exit")
        choice = input("Enter your choice: ")
        
        if choice == "1":
            name = input("Enter your name: ")
            pin = input("Create a PIN: ")
            try:
                balance = float(input("Enter initial deposit amount: "))
                print(bank.create_account(name, pin, balance))
            except ValueError:
                print("Invalid deposit amount.")

        elif choice == "2":
            account_number = input("Enter your account number: ")
            pin = input("Enter your PIN: ")
            account = bank.authenticate(account_number, pin)
            
            if account:
                print("\nLogged in successfully!")
                while True:
                    print("\n1. Check Balance")
                    print("2. Deposit")
                    print("3. Withdraw")
                    print("4. Modify Account")
                    print("5. Log out")
                    user_choice = input("Choose an option: ")
                    
                    if user_choice == "1":
                        print(account.check_balance())
                    
                    elif user_choice == "2":
                        try:
                            deposit_amount = float(input("Enter deposit amount: "))
                            print(account.deposit(deposit_amount))
                            bank.update_account(account)
                        except ValueError:
                            print("Invalid amount.")

                    elif user_choice == "3":
                        try:
                            withdraw_amount = float(input("Enter withdrawal amount: "))
                            print(account.withdraw(withdraw_amount))
                            bank.update_account(account)
                        except ValueError:
                            print("Invalid amount.")
                    
                    elif user_choice == "4":
                        new_name = input("Enter new name (or press enter to skip): ")
                        new_pin = input("Enter new PIN (or press enter to skip): ")
                        print(account.modify_account(new_name if new_name else None, new_pin if new_pin else None))
                        bank.update_account(account)

                    elif user_choice == "5":
                        print("Logging out...")
                        break
                    else:
                        print("Invalid option. Please try again.")
            else:
                print("Invalid account number or PIN.")
        
        elif choice == "3":
            print("Thank you for using the online banking system!")
            break
        else:
            print("Invalid choice. Please try again.")

#  Entry Point 
if __name__ == "__main__":
    bank_system()
