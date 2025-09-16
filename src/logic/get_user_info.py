def get_id_chamado_e_terminais():
    ticket_id = str(input("Digite o ID do chamado: "))
    n_terminais = int(input("Digite o número de terminais: "))

    return ticket_id, n_terminais


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
