"""Ponto de entrada principal para o Gerador de Fichas (versão CLI).

Este módulo fornece uma interface de linha de comando (CLI) para que o usuário
possa gerar fichas de implantação de forma interativa. Ele orquestra todo o
fluxo da aplicação, desde a coleta dos dados do usuário até o salvamento
final do arquivo .xlsx.

O fluxo de execução principal é:
1. Carrega as variáveis de ambiente necessárias (URLs, chaves de API).
2. Entra em um loop contínuo, permitindo gerar múltiplas fichas.
3. Solicita ao usuário o ID do ticket e outras informações pertinentes.
4. Realiza chamadas à API do TomTicket para buscar dados do ticket e do cliente.
5. Valida os dados recebidos das APIs utilizando schemas Pydantic.
6. Organiza os dados e os utiliza para gerar uma planilha Excel.
7. Salva o arquivo .xlsx no sistema de arquivos local.

O módulo possui tratamento de erros robusto para lidar com entradas inválidas,
falhas de comunicação com a API e dados inconsistentes.
"""

__author__ = "Mauricio Luan"
__version__ = "3.1.0"
__email__ = "mauricioluan2023@exemplo.com"
__status__ = "Production"

from time import sleep
from pydantic import ValidationError
from config.load_env import load_env
from logic.get_user_data import get_id_e_terminais, get_servico_cartao
from logic.get_tomticket_data import get_dados_ticket, get_dados_customer
from logic.gera_planilha import gera_planilha, save
from logic.monta_ficha import monta_ficha
from schemas.responses import Ticket, Customer

print(
    """
██████╗  █████╗ ██╗   ██╗███████╗██████╗
██╔══██╗██╔══██╗╚██╗ ██╔╝██╔════╝██╔══██╗
██████╔╝███████║ ╚████╔╝ █████╗  ██████╔╝
██╔══   ██║  ██╔╝  ██╔   ██╔═══╝ ██╔══██╗
██║     ██║  ██║   ██║   ███████╗██║  ██║
╚═╝     ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝
Gerador de Fichas de Implantação · 2025
"""
)


def main():
    try:
        ticket_url, customer_url, header = load_env()
    except ValueError as e:
        print(f"\nErro ao carregar variaveis de ambiente: {e}")
        print("Fechando em 2 segundos...")
        sleep(2)
        return

    while True:
        try:
            ticket_id, n_terminais = get_id_e_terminais()
            servico_cartao = get_servico_cartao()

            ticket_response = get_dados_ticket(ticket_url, ticket_id, header)
            ticket = Ticket.model_validate(ticket_response)

            protocol = ticket.data.protocol
            codigo_payer = ticket.data.customer.internal_id

            customer_response = get_dados_customer(customer_url, codigo_payer, header)
            customer = Customer.model_validate(customer_response)

            ficha = monta_ficha(protocol, customer, n_terminais, servico_cartao)
            workbook = gera_planilha(ficha)
            save(workbook, ficha)

        except ValueError as e:
            print(f"\nErro: {e}")

        except ValidationError as e:
            print(f"\nErro na modelagem dos dados: {e}")

        except Exception as e:
            print(f"\nErro inesperado: {e}")


if __name__ == "__main__":
    main()
