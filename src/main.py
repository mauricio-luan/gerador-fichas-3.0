# -*- coding: utf-8 -*-
#
# main.py, gera_planilha.py, encontra_imagem.py, config_log.py
# Projeto: Gerador de Fichas de Implantação
# Autor: Mauricio Luan
# Data de criação: 29/01/2025
# Descrição: Gera fichas de implantação para clientes, coletando dados de um chamado e formatando-os em uma planilha.
#
# Copyright (c) 2025 Payer Serviços de Pagamento LTDA. Todos os direitos reservados.

# import datetime
# import os
# from src.logic.gera_planilha import gerar_planilha_estilizada
# from src.logic.encontra_imagem import encontrar_imagem
# from src.logic.config_log import configura_logger

# log = configura_logger("gerador-fichas-3.0")


# def organiza_os_dados(response_chamado, response_cliente, n_terminais, sc):
#     """
#     Realiza o filtro das informações necessárias sobre o cliente
#     e o chamado para repassar a função que gera a planilha
#     """
#     log.debug("Iniciando a formatação dos dados...")

#     dados_chamado = response_chamado.json()
#     dados_cliente = response_cliente.json()

#     dicionario = {}

#     # Captura os dados do cliente e salva no objeto 'dicionario'
#     dados_loja = dados_cliente["data"][0]["custom_fields"]
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
from logic.load_env import load_env
from logic.get_user_info import get_id_e_terminais, get_servico_cartao
from logic.get_tomticket_data import (
    get_dados_ticket,
    get_codigo_payer,
    get_dados_customer,
)

print(
    """
██████╗  █████╗ ██╗   ██╗███████╗██████╗
██╔══██╗██╔══██╗╚██╗ ██╔╝██╔════╝██╔══██╗
██████╔╝███████║ ╚████╔╝ █████╗  ██████╔╝
██╔═══╝ ██╔══██║  ╚██╔╝  ██╔══╝  ██╔══██╗
██║     ██║  ██║   ██║   ███████╗██║  ██║
╚═╝     ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝
Gerador de Fichas de Implantação · 2025 · Mauricio Luan
"""
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

            dados_ticket = get_dados_ticket(ticket_url, ticket_id, header)
            codigo_payer = get_codigo_payer(dados_ticket)
            dados_customer = get_dados_customer(customer_url, codigo_payer, header)

            print(dados_customer)

        except ValueError as e:
            print(f"\nErro: {e}")

        except Exception as e:
            print(f"\nErro inesperado: {e}")

        # log.debug("Chama get_todos_dados()...")
        # response_chamado, response_cliente, n_terminais = get_todos_dados()
        # if not response_chamado or not response_cliente:
        #     log.warning("Reiniciando programa devido a erro nas requisições.")
        #     continue

        # sc = get_servico_cartao()

        # log.debug("Chama organiza_os_dados()")
        # planilha = organiza_os_dados(
        #     response_chamado, response_cliente, n_terminais, sc
        # )

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
    # log.debug("Aplicacao iniciada.")
    main()
