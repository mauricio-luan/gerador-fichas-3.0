"""Modulo com funções para obter dados de tickets e clientes da API TomTicket"""

import requests
from requests.exceptions import HTTPError, RequestException


def get_dados_ticket(url, ticket_id, header):
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


def get_dados_customer(url, customer_id, header):
    try:
        response = requests.get(f"{url}{customer_id}", headers=header, timeout=2)
        response.raise_for_status()

        return response.json()
    except RequestException as e:
        raise ValueError(
            f"Erro ao fazer na requisição do customer.\nDetalhes: {e}\n\n"
        ) from e
