from abc import ABC, abstractmethod
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
            print(f"withdrawal scessful of Rs. {amount}. New balance is Rs. : {self.balance}")
            return True
        else:
            print("withdrawal fail")
            return False
    
    def monthly_process(self):
        monthly_interest = self.balance * (self.interest_rate / 12)
        self.balance += monthly_interest
        print(f"monthly interest is {monthly_interest}. New balance is {self.balance}")

    def __str__(self):
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
            print(f"withdrawal scessful of Rs. {amount}. New balance is Rs. : {self.balance}")
            return True
        else:
            print(f"withdrawal fail because the loan limit exceeded of Rs. : {self.loan_limit}")
            return False
        
    
    def monthly_process(self):
       if self.balance < 0:
        self.balance -= self.fees
        print(f"Balance is negative. Deducted Rs. {self.fees}. New balance: {self.balance}")

    def __str__(self):
        return (f"Current Account [{self.account_no}] Owner: {self.owner}, "
                f"Balance: Rs. {self.balance:.2f}, Loan Limit: {self.loan_limit}")

import csv

class Bank:
    def __init__(self, name):
        self.name = name
        self.accounts = {}

    def add(self, account:Account):
        self.accounts[account.account_no] = account

    def get(self, account_no) -> Account:
        return self.accounts[account_no]

    def transfer(self, account_no_from, account_no_to, amount):
        src = self.get(account_no_from)
        dst = self.get(account_no_to)

        src.withdraw(amount)
        dst.deposit(amount)

        print(f" > {src.owner} sent {amount} pkr to {dst.owner}")


    def load_from_csv(self, file="csv_file.csv"):
        with open(file, "r") as f:
         reader = csv.DictReader(f)
         for row in reader:
            if row["account_type"] == "SavingAccount":
                acc = SavingAccount(row["Owner"], row["account_no"], float(row["balance"]), float(row["interest_rate"]))
            elif row["account_type"] == "CurrentAccount":
                acc = CurrentAccount(row["Owner"], row["account_no"], float(row["balance"]), float(row["loan_limit"]), float(row["fees"]))
            self.add(acc)

            
    def save_to_csv(self, file = "csv_file.csv"):
        cols = ["account_type", "Owner", "account_no"]
        with open(file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(cols)

            for acc in self.accounts.values():
                writer.writerow({
                acc.__class__.__name__,
                acc.owner,
                acc.account_no
                })

    def show(self):
        for acc in self.accounts.values():
            print(acc)

    def __str__(self):
        return f"Bank: {self.name}, Total Accounts: {len(self.accounts)}"


bank = Bank("Standard Charted Bank")
bank.load_from_csv("csv_file.csv")
bank.show()
print(bank)


s1 = SavingAccount("Ali", "S-123", 1000, 0.05)
c1 = CurrentAccount("Fatima", "F-321", 5000, 1000, 200)
bank.add(s1)
bank.add(c1)



bank.show()
bank.save_to_csv("csv_file.csv")
