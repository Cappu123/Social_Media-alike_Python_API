import pytest
from app.calculations import add, BankAccount, InsufficientFund

@pytest.fixture
def zero_bank_account():
    return BankAccount()

@pytest.fixture
def bank_account():
    return BankAccount(50)

@pytest.mark.parametrize("num1, num2, expected", [
    (4, 6, 10),
    (3, 5, 8),
    (12, 4, 16)
])
def test_add(num1, num2, expected):
    print("testing add function")
    assert add(num1, num2) == expected

def test_bank_account(bank_account):

    assert bank_account.balance == 50

def test_default_bank_amount(zero_bank_account):
    assert zero_bank_account.balance == 0

def test_withdraw(bank_account):
    bank_account.withdraw (20)
    assert bank_account.balance == 30

def test_deposite(bank_account):
    bank_account.deposite(20)
    assert bank_account.balance == 70

def test_collect_interest(bank_account):
    bank_account.collect_interest()
    assert round(bank_account.balance, 2) == 55


@pytest.mark.parametrize("deposited, withdrew, expected", [
    (1500, 500, 1000),
    (3400, 200, 3200)
])

def test_bank_transaction(zero_bank_account, deposited, withdrew, expected):
    zero_bank_account.deposite(deposited)
    zero_bank_account.withdraw(withdrew)
    assert zero_bank_account.balance == expected\
    

def test_insufficient_funds(bank_account):
    with pytest.raises(InsufficientFund):
        bank_account.withdraw(300)