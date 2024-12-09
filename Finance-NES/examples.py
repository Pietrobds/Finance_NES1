#Criando contas e investimentos
from Finances import  Transaction, Investment, Account, Client, generate_report, future_value_report
from datetime import datetime

Pietro = Client("pietro")
Pietro.add_account("my_account")
Investimento = Investment(1, 1000, 0.1)
Pietro.add_investment(Investimento)
Pietro.accounts[0].add_transaction(5600, 3)
Pietro.accounts[0].get_transactions(datetime(1900,5,6), datetime(2500, 5, 6))
Pietro.investments[0].calculate_value()
generate_report(Pietro)
future_value_report(Pietro, datetime(2200, 5, 6))
