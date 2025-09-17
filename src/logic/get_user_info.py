def get_id_e_terminais():
    id = input("Digite o ID do chamado: ").strip()
    n_terminais = input("Digite o número de terminais: ").strip()

    if not id or not n_terminais:
        raise ValueError("Todos os campos devem ser preenchidos.\n")

    try:
        n_terminais = int(n_terminais)
    except ValueError as e:
        raise ValueError("O número de terminais deve ser um número inteiro.\n") from e

    if n_terminais < 1:
        raise ValueError("O número de terminais deve ser maior ou igual a 1.\n")

    return id, n_terminais


def get_servico_cartao():
    opcoes = {
        1: "SC2",
        2: "SC3",
        3: "SC4",
        4: "SCS_VERO",
        5: "SCS_CIELO",
        6: "SIMULADOR",
    }
    print("\Serviços de cartão:")
    for opcao, servico in opcoes.items():
        print(f"{opcao}) {servico}")

    sc = input("Selecione a opçao: ").strip()
    try:
        sc = int(sc)
    except ValueError as e:
        raise ValueError("Valor inválido. Digite um numero inteiro.\n") from e

    servico_selecionado = opcoes.get(sc)
    if servico_selecionado is None:
        raise ValueError("Opção inválida. Digite um número dentre as opções.\n")

    return servico_selecionado
