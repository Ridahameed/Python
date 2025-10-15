from abc import ABC, abstractmethod
import csv

class Account(ABC):
    def __init__(self, owner, account_no, balance):
        self.owner = owner
        self.account_no = account_no
        self.balance = balance
    
    def deposit(self, amount):
        self.balance += amount
        print(f"Deposit of Rs. {amount} is successful. New balance is {self.balance}")

    @abstractmethod
    def withdraw(self, amount):
        pass

    @abstractmethod    
    def monthly_process(self):
        pass

class SavingAccount(Account):
    def __init__(self, owner, account_no, balance, interest_rate):
        super().__init__(owner, account_no, balance)
        self.interest_rate = interest_rate

    def withdraw(self, amount):
        if self.balance - amount >= 0:
            self.balance -= amount
            print(f"withdrawal successful of Rs. {amount}. New balance is Rs. : {self.balance:.2f}")
            return True
        else:
            print("withdrawal fail: Insufficient funds.")
            return False
    
    def monthly_process(self): 
        monthly_interest = (self.balance * self.interest_rate) / 12
        self.balance += monthly_interest
        print(f"Saving Account [{self.account_no}] monthly interest added: Rs. {monthly_interest:.2f}. New balance: {self.balance:.2f}")

    def __str__(self): # string representation
        return (f"Saving Account [{self.account_no}] Owner: {self.owner}, "
                f"Balance: Rs. {self.balance:.2f}, Rate: {self.interest_rate}")

class CurrentAccount(Account):
    def __init__(self, owner, account_no, balance, loan_limit, fees):
        super().__init__(owner, account_no, balance)
        self.loan_limit = loan_limit
        self.fees = fees
 
    def withdraw(self, amount):
        if self.balance - amount >= -self.loan_limit:
            self.balance -= amount
            print(f"withdrawal successful of Rs. {amount}. New balance is Rs. : {self.balance:.2f}")
            return True
        else:
            print(f"withdrawal fail because the loan limit exceeded of Rs. : {self.loan_limit}")
            return False
        
    
    def monthly_process(self):
        if self.balance < 0:
            self.balance -= self.fees
            print(f"Current Account [{self.account_no}] Balance is negative. Deducted Rs. {self.fees}. New balance: {self.balance:.2f}")
        else:
            print(f"Current Account [{self.account_no}] Balance is positive. No fees deducted.")

    def __str__(self): # string representation
        return (f"Current Account [{self.account_no}] Owner: {self.owner}, "
                f"Balance: Rs. {self.balance:.2f}, Loan Limit: {self.loan_limit}, Fees: {self.fees}")


class Bank:
    def __init__(self, name):
        self.name = name
        self.accounts = {}

    def add(self, account:Account):
        self.accounts[account.account_no] = account

    def get(self, account_no) -> Account:
        if account_no not in self.accounts:
            raise KeyError(f"Account number {account_no} not found.")
        return self.accounts[account_no]

    def transfer(self, account_no_from, account_no_to, amount):
        src = self.get(account_no_from)
        dst = self.get(account_no_to)

        if src.withdraw(amount):
            dst.deposit(amount)
            print(f" > {src.owner} successfully transferred Rs. {amount} to {dst.owner}")
        else:
            print(f" > Transfer of Rs. {amount} from {src.owner} to {dst.owner} failed.")


    def load_from_csv(self, file="csv_file.csv"):
        try:
            with open(file, "r") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row["account_type"] == "SavingAccount":
                        acc = SavingAccount(row["Owner"], row["account_no"], float(row["balance"]), float(row["interest_rate"]))
                    elif row["account_type"] == "CurrentAccount":
                        acc = CurrentAccount(row["Owner"], row["account_no"], float(row["balance"]), float(row["loan_limit"]), float(row["fees"]))
                    self.add(acc)
        except FileNotFoundError:
            print(f"CSV file '{file}' not found. Starting with no accounts.")
        except Exception as e:
            print(f"Error loading CSV: {e}")

            
    def save_to_csv(self, file = "csv_file.csv"):
        cols = ["account_type", "Owner", "account_no", "balance", "interest_rate", "loan_limit", "fees"]
        with open(file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(cols)

            for acc in self.accounts.values():
                row_data = [
                    acc.__class__.__name__,
                    acc.owner,
                    acc.account_no,
                    acc.balance,
                    getattr(acc, "interest_rate", ""),
                    getattr(acc, "loan_limit", ""),
                    getattr(acc, "fees", "")
                ]
                writer.writerow(row_data) 

    def show(self):
        print(f"\n--- {self.name} Account List ---")
        for acc in self.accounts.values():
            print(acc)
        print("--------------------------------\n")

    def __str__(self):
        return f"Bank: {self.name}, Total Accounts: {len(self.accounts)}"

# Example usage and testing
# Initialize bank and load accounts from CSV
initial_csv_content = """account_type,Owner,account_no,balance,interest_rate,loan_limit,fees
"""
with open("csv_file.csv", "w", newline="") as f:
    f.write(initial_csv_content)

bank = Bank("Standard Charted Bank")
bank.load_from_csv("csv_file.csv")
bank.show()
print(bank)


s1 = SavingAccount("Ali", "S-123", 1000, 0.05)
s2 = SavingAccount("Ahmed", "S-456", 2000, 0.03)
c1 = CurrentAccount("Fatima", "C-321", 5000, 1000, 200)


bank.add(s1)
bank.add(s2)
bank.add(c1)

bank.show()
bank.save_to_csv("csv_file.csv")
#-------------------------------------------------------------------------
print("--Testing Withdrawal---")
# Successful withdrawal
s1.withdraw(200)
# Failed withdrawal (Insufficient funds)
s1.withdraw(2000)
#-------------------------------------------------------------------------
print("\n--- Testing Deposit ---")
# Deposit
c1.deposit(500)
#-------------------------------------------------------------------------
print("\n--- Testing Monthly Process ---")
s1.monthly_process()
c1.monthly_process()
#-------------------------------------------------------------------------
print("\n--- Testing Transfer ---")
# Successful transfer
bank.transfer("C-321", "S-123", 500)
# Failed transfer (Ali only has 1500, trying to withdraw 2000)
bank.transfer("S-123", "C-321", 2000)