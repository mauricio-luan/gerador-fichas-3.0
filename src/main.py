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
Gerador de Fichas de Implantação · 2025 · Mauricio Luan"""
)


def main():
    try:
        ticket_url, customer_url, header = load_env()
    except ValueError as e:
        print(f"\nErro ao carregar variaveis de ambiente: {e}")
        print("Fechando em 5 segundos...")
        sleep(5)
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

            # os.startfile(pasta_razao_social)
        except ValueError as e:
            print(f"\nErro: {e}")

        except ValidationError as e:
            print(f"\nErro na modelagem dos dados: {e}")

        except Exception as e:
            print(f"\nErro inesperado: {e}")


if __name__ == "__main__":
    main()
