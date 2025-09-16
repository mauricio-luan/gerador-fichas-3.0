def get_id_e_terminais():
    id = input("Digite o ID do chamado: ").strip()
    n_terminais = input("Digite o número de terminais: ").strip()

    if not id or not n_terminais:
        raise ValueError("Todos os campos devem ser preenchidos.")

    try:
        n_terminais = int(n_terminais)
    except ValueError as e:
        raise ValueError("O número de terminais deve ser um número inteiro.") from e

    if n_terminais < 1:
        raise ValueError("O número de terminais deve ser maior ou igual a 1.")

    return id, n_terminais


def get_servico_cartao():
    print("Serviços de Cartão")
    sc = int(
        input(
            "1) SC2 2) SC3 3) SC4 4) SCS_VERO 5) SCS_CIELO 6) SIMULADOR\nSelecione a opçao: "
        )
    )
    try:
        match sc:
            case 1:
                return "SC2"
            case 2:
                return "SC3"
            case 3:
                return "SC4"
            case 4:
                return "SCS_VERO"
            case 5:
                return "SCS_CIELO"
            case 6:
                return "SIMULADOR"
            case _:
                print("toto")
                # log.info(
                #     f"Tu digitou uma opção inválida: {sc}. Foi selecionado o padrão SC2.\n"
                # )
                return "SC2"
    except Exception as e:
        print(e)
        # log.exception(f"Erro: {e}")
