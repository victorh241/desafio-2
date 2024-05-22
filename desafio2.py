
def menu():
  menu = """\n

  [d] Depositar
  [s] Sacar
  [e] Extrato
  [uv] Novo usuario
  [nc] Nova conta
  [q] Sair

  => """
  return input(menu)


def deposito(saldo,valor, extrato, /):
  if float(valor) > 0:
    saldo += valor
    extrato += f"Depósito: R$ {valor:.2f}\n"
  else:
    print("Operação falhou! O valor informado é inválido.")
  return saldo, extrato

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")

    elif excedeu_limite:
        print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")

    elif excedeu_saques:
        print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")

    elif valor > 0:
        saldo -= valor
        extrato += f"Saque:\t\tR$ {valor:.2f}\n"
        numero_saques += 1
        print("\n=== Saque realizado com sucesso! ===")

    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

    return saldo, extrato

def Mostrarextrato(saldo,/, *, extrato):
  print("\n================ EXTRATO ================")
  print("Não foram realizadas movimentações." if not extrato else extrato)
  print(f"\nSaldo: R$ {saldo:.2f}")
  print("==========================================")

def CriarUsuario(usuarios):
  nome = input("informe seu nome completo: ")
  dataNascimento = input("informe sua data de nascimento (dia-mes-ano)")
  cpf = input('informe seu cpf')

  for usuario in usuarios:
    if usuario["cpf"] == cpf:
      print("cpf já existente")
      return
  estado = input("estado que mora: ")

  cidade = input("cidade que mora: ")
  bairro = input("Bairro que mora: ")
  nro = input("número: ")
  end = f"{estado}, {cidade}, {bairro}, {nro}"

  usuarios.append({nome, dataNascimento, cpf, end})
  return usuarios

def novaConta(contas, usuarios):
  agencia = "0001"
  cpf = input("Informe o cpf")
  for usuario in usuarios:
    if usuario["cpf"] == cpf:
      numeroConta = len(contas) + 1
      return {"Agencia": agencia,"numero conta": numeroConta,"usuario ": usuario}
    print("conta ja tem o cpf registrado")


def main():
  saldo = 0
  extrato = ""
  LIMITE_SAQUES = 3
  limite = 500
  clientes = []
  contas = []
  numero_saques = 0


  while(True):
   opcao = menu()

   if(opcao == "d"):
      valor = float(input("Informe o valor do deposito: "))
      saldo, extrato = deposito(saldo, valor, extrato)
   elif opcao == "s":
      valor = float(input("Informe o valor do saque: "))

      saldo, extrato = sacar(
      saldo=saldo,
      valor=valor,
      extrato=extrato,
      limite=limite,
      numero_saques=numero_saques,
      limite_saques=LIMITE_SAQUES,)
   elif opcao == "q":
      break
   elif opcao == "e":
      Mostrarextrato(saldo, extrato=extrato)
   elif opcao == "uv":
      novoCliente = CriarUsuario(clientes)
      clientes.append(novoCliente)
   elif opcao == "nc":
    novaConta(contas, clientes)
   else:
     print('Operação inválida, por favor selecione novamente a operação desejada.')
     return

main()