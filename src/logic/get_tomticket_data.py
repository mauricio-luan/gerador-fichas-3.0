import requests
from requests.exceptions import HTTPError, RequestException


def get_dados_ticket(url, ticket_id, header) -> dict:
    try:
        response = requests.get(f"{url}{ticket_id}", headers=header, timeout=2)
        response.raise_for_status()

        return response.json()
    except HTTPError as e:
        if e.response.status_code == 404:
            raise ValueError(
                f"Ticket não encontrado. Verifique o ID e tente novamente.\nDetalhes: {e}\n\n"
            ) from e

        if e.response.status_code == 401:
            raise ValueError(f"Ação não autorizada.\nDetalhes: {e}\n\n") from e

    except RequestException as e:
        raise ValueError(
            f"Erro ao fazer a requisição do ticket.\nDetalhes: {e}\n\n"
        ) from e


def get_codigo_payer(data):
    try:
        return data["data"]["customer"]["internal_id"]
    except KeyError as e:
        raise ValueError(f"Erro ao obter o código Payer.\nDetalhes: {e}\n\n") from e


def get_dados_customer(url, customer_id, header) -> dict:
    try:
        response = requests.get(f"{url}{customer_id}", headers=header, timeout=2)
        response.raise_for_status()

        return response.json()
    except RequestException as e:
        raise ValueError(
            f"Erro ao fazer na requisição do customer.\nDetalhes: {e}\n\n"
        ) from e

    #         return response_ticket, conta_empresa_loja, n_terminais

    #     else:
    #         # log.error(
    #             f"Retorno da requisição do ticket: {response_ticket.status_code}: {response_ticket.reason}"
    #         )

    # except requests.exceptions.RequestException as e:
    #     # log.exception(f"Erro ao fazer a requisição do ticket: {e}")
    #     # log.info("Erro ao obter dados do ticket. Verifique o ID e tente novamente.")
    #     return None, None, None


# def get_dados_cliente(headers, conta_empresa_loja):
#     try:
#         # log.debug("Consultando dados do cliente...")
#         response_cliente = requests.get(
#             f"{API_URL}{conta_empresa_loja}", headers=headers, timeout=2
#         )

#         if response_cliente.status_code == 200:
#             log.debug("Requisicao do cliente bem sucedida.")

#             dados_cliente = response_cliente.json()
#             log.debug(f"Dados do cliente: {dados_cliente}")

#             return response_cliente
#         else:
#             log.error(
#                 f"Retorno da requisição do cliente: {response_cliente.status_code}: {response_cliente.reason}"
#             )
#             return None

#     except requests.exceptions.RequestException as e:
#         log.exception(f"Erro ao fazer a requisição do cliente: {e}")
#         log.info(
#             "Erro ao obter dados do cliente. Verifique o conta_empresa_loja e tente novamente."
#         )
#         return None
