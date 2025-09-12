# -*- coding: utf-8 -*-
#
# main.py, gera_planilha.py, encontra_imagem.py, config_log.py
# Projeto: Gerador de Fichas de Implantação
# Autor: Mauricio Luan
# Data de criação: 29/01/2025
# Descrição: Gera fichas de implantação para clientes, coletando dados de um chamado e formatando-os em uma planilha.
#
# Copyright (c) 2025 Payer Serviços de Pagamento LTDA. Todos os direitos reservados.

import datetime
import os
import requests
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
    headers = {"Authorization": f"Bearer {API_TOKEN}"}

    log.debug("Variaveis de ambiente carregadas.")

except Exception as e:
    log.exception(f"Erro ao carregar variaveis de ambiente: {e}")
    log.error("Erro ao carregar as variaveis de ambiente. Verifique o arquivo .env.")


def get_id_chamado_e_terminais():
    ticket_id = str(input("Digite o ID do chamado: "))
    n_terminais = int(input("Digite o número de terminais: "))

    return ticket_id, n_terminais


def get_servico_cartao():
    print("Serviços de Cartão")
    sc = int(
        input(
            "1) SC2 2) SC3 3) SC4 4) SCS_VERO 5) SCS_CIELO 6) SIMULADOR\nSelecione a opçao: "
        )
    )
    try:
        match sc:
            case 1:
                return "SC2"
            case 2:
                return "SC3"
            case 3:
                return "SC4"
            case 4:
                return "SCS_VERO"
            case 5:
                return "SCS_CIELO"
            case 6:
                return "SIMULADOR"
            case _:
                log.info(
                    f"Tu digitou uma opção inválida: {sc}. Foi selecionado o padrão SC2.\n"
                )
                return "SC2"
    except Exception as e:
        log.exception(f"Erro: {e}")


def get_dados_chamado(headers):
    ticket_id, n_terminais = get_id_chamado_e_terminais()

    try:
        log.info("Consultando dados do chamado...")
        response_chamado = requests.get(
            f"{API_TICKET_URL}{ticket_id}", headers=headers, timeout=2
        )

        if response_chamado.status_code == 200:
            log.debug("Requisicao do chamado bem sucedida.")

            dados_chamado = response_chamado.json()
            log.debug(f"Dados do chamado: {dados_chamado}")

            # captura do conta-empresa-loja para uso em 'get_dados_cliente'
            conta_empresa_loja = dados_chamado["data"]["customer"]["internal_id"]

            return response_chamado, conta_empresa_loja, n_terminais

        else:
            log.error(
                f"Retorno da requisição do chamado: {response_chamado.status_code}: {response_chamado.reason}"
            )

    except requests.exceptions.RequestException as e:
        log.exception(f"Erro ao fazer a requisição do chamado: {e}")
        log.info("Erro ao obter dados do chamado. Verifique o ID e tente novamente.")
        return None, None, None


def get_dados_cliente(headers, conta_empresa_loja):
    try:
        log.info("Consultando dados do cliente...")
        response_cliente = requests.get(
            f"{API_URL}{conta_empresa_loja}", headers=headers, timeout=2
        )

        if response_cliente.status_code == 200:
            log.debug("Requisicao do cliente bem sucedida.")

            dados_cliente = response_cliente.json()
            log.debug(f"Dados do cliente: {dados_cliente}")

            return response_cliente
        else:
            log.error(
                f"Retorno da requisição do cliente: {response_cliente.status_code}: {response_cliente.reason}"
            )
            return None

    except requests.exceptions.RequestException as e:
        log.exception(f"Erro ao fazer a requisição do cliente: {e}")
        log.info(
            "Erro ao obter dados do cliente. Verifique o conta_empresa_loja e tente novamente."
        )
        return None


def get_todos_dados():
    response_chamado, conta_empresa_loja, n_terminais = get_dados_chamado(headers)
    response_cliente = get_dados_cliente(headers, conta_empresa_loja)

    return response_chamado, response_cliente, n_terminais


def organiza_os_dados(response_chamado, response_cliente, n_terminais, sc):
    log.info("Iniciando a formatação dos dados...")
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
        "Serviço Cartão": str(sc),
    }
    log.debug(f"Dados organizados: {planilha}")

    return planilha


def definir_contexto_salvamento(planilha):
    caminho_base = f"G:\\Drives compartilhados\\FICHAS DE IMPLANTACAO"

    try:
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

        return arquivo_excel, caminho_imagem, pasta_razao_social

    except Exception as e:
        log.exception(f"Erro ao definir contexto de salvamento: {e}")
        return None, None, None


def main():
    while True:
        log.debug("Chama get_todos_dados()...")
        response_chamado, response_cliente, n_terminais = get_todos_dados()
        if not response_chamado or not response_cliente:
            log.warning("Reiniciando programa devido a erro nas requisições.")
            continue

        sc = get_servico_cartao()

        log.debug("Chama organiza_os_dados()")
        planilha = organiza_os_dados(
            response_chamado, response_cliente, n_terminais, sc
        )

        arquivo_excel, caminho_imagem, pasta_razao_social = definir_contexto_salvamento(
            planilha
        )
        if not arquivo_excel or not caminho_imagem or not pasta_razao_social:
            log.warning("Reiniciando programa devido a erro no contexto de salvamento.")
            continue

        log.debug("Chama gerar_planilha_estilizada()")
        gerar_planilha_estilizada(planilha, arquivo_excel, caminho_imagem)

        log.info("Abrindo pasta.")
        os.startfile(pasta_razao_social)


if __name__ == "__main__":
    log.info("Aplicacao iniciada.")
    main()
