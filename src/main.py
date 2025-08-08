# -*- coding: utf-8 -*-
#
# main.py, gera_planilha.py, encontra_imagem.py, config_log.py
# Projeto: Gerador de Fichas de Implantação
# Autor: Mauricio Luan
# Data de criação: 29/01/2025
# Descrição: Gera fichas de implantação para clientes, coletando dados de um chamado e formatando-os em uma planilha.
#
# Copyright (c) 2025 Payer Serviços de Pagamento LTDA. Todos os direitos reservados.

import requests
import datetime
import os
from dotenv import load_dotenv
from gera_planilha import gerar_planilha_estilizada
from encontra_imagem import encontrar_imagem
from config_log import configura_logger

log = configura_logger("gerador-fichas-3.0")

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

load_dotenv()

log.debug("Carregando variaveis de ambiente...")
try:
    API_URL = os.getenv("API_URL")
    API_TICKET_URL = os.getenv("API_TICKET_URL")
    API_TOKEN = os.getenv("API_TOKEN")
    log.debug("Variaveis de ambiente carregadas.")
    headers = {"Authorization": f"Bearer {API_TOKEN}"}

except Exception as e:
    log.exception(f"Erro ao carregar variaveis de ambiente: {e}")
    log.error("Erro ao carregar as variaveis de ambiente. Verifique o arquivo .env.")


def get_dados(headers):
    ticket_id = input("Digite o ID do chamado: ")
    n_terminais = input("Digite o número de terminais: ")

    try:
        log.info("Consultando dados do chamado...")
        response_chamado = requests.get(
            f"{API_TICKET_URL}{ticket_id}", headers=headers, timeout=2
        )

        if response_chamado.status_code == 200:
            log.info("Requisicao do chamado bem sucedida.")

            dados_chamado = response_chamado.json()
            log.debug(f"Dados do chamado: {dados_chamado}")

            # captura do conta-empresa-loja
            conta_empresa_loja = dados_chamado["data"]["customer"]["internal_id"]

            log.info("Consultando dados do cliente...")
            response_cliente = requests.get(
                f"{API_URL}{conta_empresa_loja}", headers=headers, timeout=2
            )

            return response_chamado, response_cliente, n_terminais
        else:
            log.error(
                f"Retorno da requisição do chamado: {response_chamado.status_code} - {response_chamado.reason}"
            )

    except requests.exceptions.RequestException as e:
        log.exception(f"Erro ao fazer a requisição do chamado: {e}")
        log.info("Erro ao obter dados do chamado. Verifique o ID e tente novamente.")
        return None, None, None


def organiza_os_dados(response_chamado, response_cliente, n_terminais):
    """
    Realiza o filtro das informações necessárias sobre o cliente
    e o chamado para repassar a função que gera a planilha
    """

    dados_chamado = response_chamado.json()
    dados_cliente = response_cliente.json()

    dicionario = {}

    # Captura os dados do cliente e salva no objeto 'dicionario'
    dados_loja = dados_cliente["data"][0]["custom_fields"]
    dados_a_capturar = [
        "Nome Fantasia",
        "CNPJ",
        "Endereco",
        "Numero",
        "Bairro",
        "Cidade",
        "COMERCIAL - Contato",
        "COMERCIAL - Telefone",
        "COMERCIAL - E-mail",
    ]
    for campo in dados_a_capturar:
        for item in dados_loja:
            if item["name"] == campo:
                dicionario[campo] = item["value"]

    # captura numero do chamado e razão social do cliente
    chamado = dados_chamado["data"]["protocol"]
    razao_social = dados_chamado["data"]["customer"]["name"].strip()

    # captura conta empresa loja e formata para exibição na planilha
    conta_empresa_loja = dados_cliente["data"][0]["internal_id"]
    conta, empresa, loja = conta_empresa_loja.split("-")
    dicionario["Conta"] = f"{conta} - {razao_social}"
    dicionario["Empresa"] = f"{empresa} - {razao_social}"
    dicionario["Loja"] = f"{loja} - {dicionario['Nome Fantasia']}"

    # gera os tokens para a quantidade de terminais
    partes = conta_empresa_loja.split("-")
    tokens = []
    for i in range(1, int(n_terminais) + 1):
        tokens.append(f"{partes[1]}{partes[2]}{str(i).zfill(2)}")

    # esse objeto representa a planilha que será preenchida.
    # as chaves representam as celulas da primeira coluna e
    # os valores são os dados que serão preenchidos
    data = datetime.date.today()

    planilha = {
        "Chamado": str(chamado) + " - " + str(data.strftime("%d/%m/%Y")),
        "Nome Fantasia": dicionario["Nome Fantasia"],
        "Razão Social": razao_social,
        "CNPJ": dicionario.get("CNPJ", ""),
        "Endereco": str(dicionario.get("Endereco", "") or "").upper()
        + ", "
        + str(dicionario.get("Numero", "") or "").upper(),
        "Bairro": str(dicionario.get("Bairro", "")).upper(),
        "Cidade": str(dicionario.get("Cidade", "")).upper(),
        "Contato": str(dicionario.get("COMERCIAL - Contato", "")).upper(),
        "Telefone": dicionario.get("COMERCIAL - Telefone", ""),
        "E-mail": dicionario.get("COMERCIAL - E-mail", ""),
        "Conta": dicionario["Conta"],
        "Empresa": dicionario["Empresa"],
        "Loja": dicionario["Loja"],
        "Token Payer": " / ".join(tokens),
    }
    log.debug(f"Dados organizados: {planilha}")

    return planilha


if __name__ == "__main__":
    log.info("Aplicacao iniciada.")
    while True:
        log.info("chama get_dados()")
        response_chamado, response_cliente, n_terminais = get_dados(headers)
        if not response_chamado or not response_cliente:
            log.warning("Reiniciando programa devido a erro nas requisições.")
            continue

        log.info("chama organiza_os_dados()")
        planilha = organiza_os_dados(response_chamado, response_cliente, n_terminais)

        # salva tudão
        caminho_base = f"G:\\Drives compartilhados\\FICHAS DE IMPLANTACAO"
        if not os.path.exists(caminho_base):
            caminho_base = os.path.join(os.path.expanduser("~"), "Documents")
            log.info(
                f"Caminho do google drive nao encontrado. Salvando em: {caminho_base}\n"
            )

        primeira_letra = planilha["Razão Social"][0].upper()
        subpasta_letra = os.path.join(caminho_base, primeira_letra)
        os.makedirs(subpasta_letra, exist_ok=True)
        pasta_razao_social = os.path.join(subpasta_letra, planilha["Razão Social"])
        os.makedirs(pasta_razao_social, exist_ok=True)
        arquivo_excel = os.path.join(pasta_razao_social, f"{planilha['Loja']}.xlsx")

        caminho_imagem = encontrar_imagem("payer.png")

        log.info("Chama gerar_planilha_estilizada()")
        gerar_planilha_estilizada(planilha, arquivo_excel, caminho_imagem)

        log.info("Abrindo pasta.")
        os.startfile(pasta_razao_social)
