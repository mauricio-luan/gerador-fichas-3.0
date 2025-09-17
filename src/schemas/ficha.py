from pydantic import BaseModel
from typing import Optional
from schemas.ticket import Ticket
from schemas.customer import Customer


class Ficha(BaseModel):
    chamado: str
    nome_fantasia: str
    razao_social: str
    cnpj: str
    endereco: Optional[str] = None
    bairro: Optional[str] = None
    cidade: Optional[str] = None
    contato: str
    telefone: Optional[str] = None
    email: str
    account: str
    company: str
    store: str
    token: str
    servico_cartao: Optional[str] = None


def dados_model_validate(ticket, customer) -> tuple[Ticket, Customer]:
    ticket_validate = Ticket.model_validate(ticket)
    customer_validate = Customer.model_validate(customer)

    return ticket_validate, customer_validate


# def monta_ficha(
#     dados_ticket: Ticket, dados_customer: Customer, n_terminais, servico_cartao
# ):

#     dados_a_capturar = [
#         "Nome Fantasia",
#         "CNPJ",
#         "Endereco",
#         "Numero",
#         "Bairro",
#         "Cidade",
#         "COMERCIAL - Contato",
#         "COMERCIAL - Telefone",
#         "COMERCIAL - E-mail",
#     ]
#     for campo in dados_a_capturar:
#         for item in dados_loja:
#             if item["name"] == campo:
#                 dicionario[campo] = item["value"]

#     # captura numero do chamado e razão social do cliente
#     chamado = dados_chamado["data"]["protocol"]
#     razao_social = dados_chamado["data"]["customer"]["name"].strip()

#     # captura conta empresa loja e formata para exibição na planilha
#     conta_empresa_loja = dados_cliente["data"][0]["internal_id"]
#     conta, empresa, loja = conta_empresa_loja.split("-")
#     dicionario["Conta"] = f"{conta} - {razao_social}"
#     dicionario["Empresa"] = f"{empresa} - {razao_social}"
#     dicionario["Loja"] = f"{loja} - {dicionario['Nome Fantasia']}"

#     # gera os tokens para a quantidade de terminais
#     partes = conta_empresa_loja.split("-")
#     tokens = []
#     for i in range(1, int(n_terminais) + 1):
#         tokens.append(f"{partes[1]}{partes[2]}{str(i).zfill(2)}")

#     # esse objeto representa a planilha que será preenchida.
#     # as chaves representam as celulas da primeira coluna e
#     # os valores são os dados que serão preenchidos
#     data = datetime.date.today()

#     planilha = {
#         "Chamado": str(chamado) + " - " + str(data.strftime("%d/%m/%Y")),
#         "Nome Fantasia": dicionario["Nome Fantasia"],
#         "Razão Social": razao_social,
#         "CNPJ": dicionario.get("CNPJ", ""),
#         "Endereco": str(dicionario.get("Endereco", "") or "").upper()
#         + ", "
#         + str(dicionario.get("Numero", "") or "").upper(),
#         "Bairro": str(dicionario.get("Bairro", "")).upper(),
#         "Cidade": str(dicionario.get("Cidade", "")).upper(),
#         "Contato": str(dicionario.get("COMERCIAL - Contato", "")).upper(),
#         "Telefone": dicionario.get("COMERCIAL - Telefone", ""),
#         "E-mail": dicionario.get("COMERCIAL - E-mail", ""),
#         "Conta": dicionario["Conta"],
#         "Empresa": dicionario["Empresa"],
#         "Loja": dicionario["Loja"],
#         "Token Payer": " / ".join(tokens),
#         "Serviço Cartão": str(sc),
#     }
#     log.debug(f"Dados organizados: {planilha}")

#     return planilha
