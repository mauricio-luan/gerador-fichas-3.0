# def definir_contexto_salvamento(planilha):
#     caminho_base = f"G:\\Drives compartilhados\\FICHAS DE IMPLANTACAO"
#     try:
#         if not os.path.exists(caminho_base):
#             caminho_base = os.path.join(os.path.expanduser("~"), "Documents")
#             log.info(
#                 f"Caminho do google drive nao encontrado. Salvando em: {caminho_base}\n"
#             )
#         primeira_letra = planilha["Razão Social"][0].upper()
#         subpasta_letra = os.path.join(caminho_base, primeira_letra)
#         os.makedirs(subpasta_letra, exist_ok=True)
#         pasta_razao_social = os.path.join(subpasta_letra, planilha["Razão Social"])
#         os.makedirs(pasta_razao_social, exist_ok=True)
#         arquivo_excel = os.path.join(pasta_razao_social, f"{planilha['Loja']}.xlsx")
#         caminho_imagem = encontrar_imagem("payer.png")
#         return arquivo_excel, caminho_imagem, pasta_razao_social
#     except Exception as e:
#         log.exception(f"Erro ao definir contexto de salvamento: {e}")
#         return None, None, None

from time import sleep
from pydantic import ValidationError
from config.load_env import load_env
from logic.get_user_info import get_id_e_terminais, get_servico_cartao
from logic.get_tomticket_data import get_dados_ticket, get_dados_customer
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
            print(f"{ficha}")
        except ValueError as e:
            print(f"\nErro: {e}")

        except ValidationError as e:
            print(f"\nErro de validacao dos dados: {e}")

        except Exception as e:
            print(f"\nErro inesperado: {e}")

        # arquivo_excel, caminho_imagem, pasta_razao_social = definir_contexto_salvamento(
        #     planilha
        # )
        # if not arquivo_excel or not caminho_imagem or not pasta_razao_social:
        #     log.warning("Reiniciando programa devido a erro no contexto de salvamento.")
        #     continue

        # log.debug("Chama gerar_planilha_estilizada()")
        # gerar_planilha_estilizada(planilha, arquivo_excel, caminho_imagem)

        # log.debug("Abrindo pasta.")
        # os.startfile(pasta_razao_social)


if __name__ == "__main__":
    main()
