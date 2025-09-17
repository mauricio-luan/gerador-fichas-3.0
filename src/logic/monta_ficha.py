from schemas.responses import Customer


def monta_ficha(
    protocol: str, customer: Customer, n_terminais: int, servico_cartao: str
):
    razao_social = customer.data[0].name.strip()

    return razao_social, protocol, n_terminais, servico_cartao
