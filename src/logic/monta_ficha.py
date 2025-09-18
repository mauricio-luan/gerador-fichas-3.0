import datetime
from pydantic import ValidationError
from schemas.responses import Customer
from schemas.ficha import Ficha


def token(codigo_payer, n_terminais) -> list[str]:
    partes = codigo_payer.split("-")
    tokens = []

    for i in range(1, int(n_terminais) + 1):
        tokens.append(f"{partes[1]}{partes[2]}{str(i).zfill(2)}")
    return tokens


def monta_ficha(
    protocol: int, customer: Customer, n_terminais: int, servico_cartao: str
) -> Ficha:
    if not customer.data:
        raise ValueError("Campo 'data' de customer está vazio.")

    codigo_payer = customer.data[0].internal_id
    conta, empresa, loja = codigo_payer.split("-")

    tokens = token(codigo_payer, n_terminais)

    custom_fields = customer.data[0].custom_fields
    linhas = {objeto.name: objeto.value for objeto in custom_fields}

    chamado = f"{protocol} - {datetime.date.today().strftime('%d/%m/%Y')}"
    fantasia_bruto = linhas.get("Nome Fantasia")
    nome_fantasia = fantasia_bruto.strip() if fantasia_bruto else "Nao informado"
    razao_social = customer.data[0].name.strip().upper()
    cnpj_bruto = linhas.get("CNPJ")
    cnpj = cnpj_bruto.strip() if cnpj_bruto else "Nao informado"
    endereco_bruto = f"{linhas.get("Endereco")}, {linhas.get('Numero')}"
    endereco = endereco_bruto.strip().upper() if endereco_bruto else "Nao informado"
    bairro_bruto = linhas.get("Bairro")
    bairro = bairro_bruto.strip().upper() if bairro_bruto else "Nao informado"
    cidade_bruto = f"{linhas.get('Cidade')}, {linhas.get('UF')}"
    cidade = cidade_bruto.strip().upper() if cidade_bruto else "Nao informado"
    contato_bruto = linhas.get("COMERCIAL - Contato")
    contato = contato_bruto.strip().upper() if contato_bruto else "Nao informado"
    telefone_bruto = linhas.get("COMERCIAL - Telefone")
    telefone = telefone_bruto if telefone_bruto else "Nao informado"
    email_bruto = linhas.get("COMERCIAL - E-mail")
    email = email_bruto.strip() if email_bruto else "Nao informado"

    try:
        ficha = Ficha(
            chamado=chamado,
            nome_fantasia=nome_fantasia,
            razao_social=razao_social,
            cnpj=cnpj,
            endereco=endereco,
            bairro=bairro,
            cidade=cidade,
            contato=contato,
            telefone=telefone,
            email=email,
            account=f"{conta} - {razao_social}",
            company=f"{empresa} - {razao_social}",
            store=f"{loja} - {nome_fantasia}",
            token="/".join(tokens),
            servico_cartao=servico_cartao,
        )
        return ficha
    except ValidationError as e:
        raise ValueError(f"Erro de validação ao criar ficha.\nDetalhes {e}\n\n") from e
