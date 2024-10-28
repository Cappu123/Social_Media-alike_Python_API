def add(num1: int, num2: int):
    return num1 + num2

class InsufficientFund(Exception):
    pass

class BankAccount():
    def __init__(self, starting_balance = 0):
        self.balance = starting_balance

    def deposite(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if amount > self.balance:
            raise InsufficientFund("Insefficient balance")
        self.balance -= amount

    def collect_interest(self):
        self.balance *= 1.1
