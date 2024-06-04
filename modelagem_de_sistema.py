from abc import ABC, abstractmethod
from datetime import datetime as dt
import textwrap


class Cliente:
    def __init__(self, endereco) -> None:
        self.contas = []
        self.endereco = endereco
    
    def trasicao(self, conta, Trasisacao):
        Trasisacao.registrar()
    
    def addConta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, contas, endereco, cpf, nome, data_nascimento) -> None:
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento

class Conta:
    #contem saldo como privado
    def __init__(self, numero, cliente) -> None:
        self._saldo = 0#variavel privada
        self._agencia = "0001"#variavel privada
        self._numero = numero#variavel privada
        self._cliente = cliente#variavel privada
        self._historico = Historico()
    
    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)
        
    @property
    def saldo(self):
        return self._saldo
        
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self.cliente
    
    @property
    def historico(self):
        return self._historico

    def depositar(self, valor: float):
        if valor > 0:
            self._saldo += valor
            print("deposito feito")
        else:
            print("Operação invalida")
            return False
        
        return True


    
    def sacar(self, valor: float):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
        elif valor > 0:
            self._saldo -= valor
            return True
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite = 500, limite_saque = 3) -> None:
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saque = limite_saque
    
    def sacar(self,valor):
        numero_saques = len(
            [Trasisacao for Trasisacao in self.historico.trasacoes
            if Trasisacao["tipo"] == saque.__name__ ]
        )

        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques > self.limite_saque

        if excedeu_limite:
            print("Valor superou o limite")
        elif excedeu_saques:
            print("excedeu limite de saques")
        else:
            super.sacar(valor)
        return False

    def __str__(self) -> str:
        return f"""
            Agência:\t{self.agencia} 
            C\C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """

class Historico(Conta):
    def __init__(self):
        self._trasisoes = []
    
    @property
    def transacoes(self):
        return self._trasisoes

    def adcionar_transacoes(self, trasicoes):
        trasicoes.append(
            {
                "tipo": Trasisacao.__class__.__name__,
                "valor": Trasisacao.valor,
                "data": dt.now().strftime("%d-%m-%Y %H:%M:%s"),
            }
        )  

class Trasisacao(ABC):
    @property
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass

class saque(Trasisacao):
    def __init__(self, valor):
        self._valor = valor
    
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historica.adcionar_transacoes(self)
    
class Deposito(Trasisacao):
    def __init__(self, valor):
        self._valor = valor
    
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historica.adcionar_transacoes(self)

def menu():
    menu = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))


def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None


def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\n@@@ Cliente não possui conta! @@@")
        return

    # FIXME: não permite cliente escolher a conta
    return cliente.contas[0]


def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)


def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    valor = float(input("Informe o valor do saque: "))
    transacao = saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)


def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print("\n================ EXTRATO ================")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"

    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("==========================================")


def criar_cliente(clientes):
    cpf = input("Informe o CPF (somente número): ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("\n@@@ Já existe cliente com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)

    clientes.append(cliente)

    print("\n=== Cliente criado com sucesso! ===")


def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado, fluxo de criação de conta encerrado! @@@")
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print("\n=== Conta criada com sucesso! ===")


def listar_contas(contas):
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))


def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            depositar(clientes)

        elif opcao == "s":
            sacar(clientes)

        elif opcao == "e":
            exibir_extrato(clientes)

        elif opcao == "nu":
            criar_cliente(clientes)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("\n@@@ Operação inválida, por favor selecione novamente a operação desejada. @@@")


main()