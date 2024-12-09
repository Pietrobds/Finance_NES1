from datetime import datetime
from dateutil.relativedelta import relativedelta

class Transaction:
    CATEGORIES = {
        1: "Pagamento",
        2: "Transferência",
        3: "Depósito"
    }
    def __init__(self, amount: float, category: str, description: str="") -> None:
        """Inicializa uma transação com valor, categoria, descrição e a data sendo a de instância.

        Args:
            amount(float): valor da transação.
            category(int): categoria a qual a transação pertence.
            description(str): descrição sobre a transação.
        """
        if category not in self.CATEGORIES.keys():
            raise ValueError("Categoria inválida")
        self.amount = amount
        self.category = category
        self.description = description
        self.date = datetime.now()
    
    def __str__(self) -> str:
        """Retorna uma descrição da transação."""
        return f"Transação: {self.description} R${self.amount} {self.CATEGORIES[self.category]}"
    
    def update(
        self,
        amount: float | None=None,
        category: int | None=None,
        description: str | None=None,
        date: datetime | None=None
    ) -> None:
        """Atualiza uma ou mais informações iniciais da transação.

        Args:
            amount(float | None): Novo valor dá transação, ou None se não for atualizar.
            category(int | None): Nova categoria dá transação, ou None se não for atualizar.
            description(str | None): Nova descrição dá transação, ou None se não for atualizar.
            date(datetime | None): Nova data dá transação, ou None se não for atualizar.
        """
        if amount != None:
            self.amount = amount
        if category != None:
            if category not in self.CATEGORIES.keys():
                raise ValueError("Categoria inválida")
            self.category = category
        if description != None:
            self.description = description
        if date != None:
            self.date = date


class Account:
    #definindo o cliente como um atributo de classe para ser modificado por metódos do cliente
    client = None
    def __init__(self, name: str) -> None:
        """Inicializa uma Conta, com nome, saldo inicial definido como 0,00 e uma lista de transações vazia.

        Args:
            name(str): Nome da conta.
        """
        self.name = name
        self.balance = 0.00
        self.transactions = []
    
    def add_transaction(self, amount: float, category: int, description: str="") -> Transaction:
        """Cria uma transação e adiciona a lista de transações da conta, e atualiza o saldo.

        Args:
            amount(float): Valor da transação.
            category(int): Categoria da transação.
            description(str): descrição da transação, definido como "".
        
        Returns:
            Transaction: Retorna a transação criada para adicionar a conta.
        """
        transaction = Transaction(amount, category, description)
        self.transactions.append(transaction)
        #Se a categoria for depósito, adiciona ao saldo, se for Pagamento ou transferência ele subtrai do saldo.
        if category == 3:
            self.balance += amount
        else:
            if self.balance - amount >= 0.00:
                self.balance -= amount
            #A conta não pode ficar negativa, se ficar força um ValueError.
            else:
                raise ValueError("O valor a ser retirado da conta têm que ser menor do que o saldo da conta")
        return transaction
    
    def get_transactions(
            self,
            start_date: datetime | None=None,
            end_date: datetime | None=None, 
            category: int | None=None
        ) -> list[Transaction]:
        """Cria uma lista com as transções, seguindo data inicial, data final e categoria.

        Args:
            start_data(datetime | None): data inicial para entrar na lista, ou None se não precisar.
            end_data(datetime | None): data final para entrar na lista, ou None se não precisar.
            category(int | None): categoria para entrar na lista, ou None se não precisar.
        
        Returns:
            list[Transaction]: Retorna a lista que foi criada.
        """
        #define a lista igual a da conta, depois vai apagando conforme as especificações
        list_transactions = self.transactions.copy()
        if start_date != None:
            for transaction in list_transactions:
                if transaction.date < start_date:
                    list_transactions.pop(transaction)
        if end_date != None:
            for transaction in list_transactions:
                if transaction.date > end_date:
                    list_transactions.pop(transaction)
        if category != None:
            for transaction in list_transactions:
                if transaction.category != category:
                    list_transactions.pop(transaction)
        return list_transactions
       
        
class Investment:
    #definindo o cliente como um atributo de classe para ser modificado por metódos do cliente
    client = None
    def __init__(self, type: int, amount: float, rate_of_return: float) -> None:
        """Inicializa um investimento com tipo, valor, porcentagem de retorno, e define a data da instância.

        Args:
            type(int): tipo do investimento.
            amount(float): valor investido.
            rate_of_return(float): porcentagem de retorno do investimento.
        """
        self.type = type
        self.initial_amount = amount
        self.date_purchased = datetime.now()
        self.rate_of_return = rate_of_return
    
    def calculate_value(self) -> float:
        """Calcula o valor que atual do investimento.
        
        Returns:
            float: Retorna o valor atual do investimento.
        """
        data_agora = datetime.now()
        #Pegando os meses e anos de diferenças entre a data do investimento, e a atual e transformando ano em meses.
        tempo_investimento = relativedelta(data_agora, self.date_purchased)
        meses_investimentos = tempo_investimento.years * 12 + tempo_investimento.months
        valor_total = self.initial_amount
        #Para cada mês que se passou adiciona a porcentagem de retorno do investimento
        for num in range(meses_investimentos):
            valor_total += (valor_total*self.rate_of_return)
        return valor_total
    
    def sell(self, account: Account) -> None:
        """Vende o investimento, definindo o valor como 0,00 e adiciona a uma conta.

        Args:
            account(Account): conta para qual o valor vai ser transferido.
        """
        account.balance += self.calculate_value()
        self.initial_amount = 0.00


class Client:
    def __init__(self, name: str) -> None:
        """Inicializa um Cliente com nome, e lista de contas e investimentos vazias.

        Args:
            name(str): Nome do cliente.
        """
        self.name = name
        self.accounts = []
        self.investments = []
    
    def add_account(self, account_name: str) -> Account:
        """Cria uma conta e adiciona a lista de conta do cliente.

        Args:
            account_name(str): Nome da conta a ser criada.
        
        Returns:
            Account: Retorna a conta criada.
        """
        account_now = Account(account_name)
        #definindo o atributo de classe cliente da conta como esse cliente
        account_now.client = self.name
        self.accounts.append(account_now)
    
    def add_investment(self, investment: Investment) -> None:
        """Adiciona um investimento a lista de investimentos do cliente.

        Args:
            investment(Investment): investimento para ser adicionado a conta.
        """
        #definindo o atributo de classe cliente do investimento como esse cliente.
        investment.client = self.name
        self.investments.append(investment)
    
    def get_net_worth(self) -> float:
        """Calcula o valor total acumulado nas contas e investimentos do cliente.

        Returns:
            float: Retorna o valor total acumulado nas contas e investimentos do cliente.
        """
        valor_total = 0
        #somando o valor das contas e investimentos
        for account in self.accounts:
            valor_total += account.balance
        for investment in self.investments:
            valor_total += investment.calculate_value()
        return valor_total


def generate_report(client: Client) -> None:
    """Faz um relatório completo de valores nas contas do cliente.
    
    Args:
        client(Client): cliente para o qual o relatório será feito.
    """
    for account in client.accounts:
        print(f"Relatório na sua conta {client.accounts.index(account)}\n\n")
        for transaction in account.transactions:
            print(f"    {transaction}\n")
        print(f"Saldo final na conta: {account.balance}")
    for investment in client.investments:
        print(f"Relatório do seu investimento {client.investments.index(investment)}:\n")
        print(f"  Valor do investimento: {investment.calculate_value()}")
    print(f"Valor Total das sua contas e investimentos: {client.get_net_worth()}")

def future_value_report(client: Client, date: datetime) -> None:
    """Faz o levantamento de quanto dinheiro terão acumulados nos investimentos do cliente.

    Args:
        client(Client): cliente para qual o levantamento será feito.
        date(datetime): data que o cliente quer ver como estarão seus investimentos.
    """
    valor_total = 0
    #Mesma conta que lá em cima, só com variáveis diferentes.
    for investment in client.investments:
        tempo_investimento = relativedelta(investment.date_purchased, date)
        meses_investimentos = tempo_investimento.years * 12 + tempo_investimento.months
        valor_investimento = investment.initial_amount
        for num in range(meses_investimentos):
            valor_investimento += (valor_total*investment.rate_of_return)
        valor_total += valor_investimento
        print(f"O valor do investimento {client.investments.index(investment)} na data prevista será de: {valor_investimento}")
    print(f"\n\n  Logo o valor que você terá em investimentos é de {valor_total}")
