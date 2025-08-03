import requests
import datetime
import os
from dotenv import load_dotenv
from gera_planilha import gerar_planilha_estilizada
from encontra_imagem import encontrar_imagem

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

API_URL = os.getenv("API_URL")
API_TICKET_URL = os.getenv("API_TICKET_URL")
API_TOKEN = os.getenv("API_TOKEN")

headers = {"Authorization": f"Bearer {API_TOKEN}"}

print("""
██████╗  █████╗ ██╗   ██╗███████╗██████╗ 
██╔══██╗██╔══██╗╚██╗ ██╔╝██╔════╝██╔══██╗
██████╔╝███████║ ╚████╔╝ █████╗  ██████╔╝
██╔═══╝ ██╔══██║  ╚██╔╝  ██╔══╝  ██╔══██╗
██║     ██║  ██║   ██║   ███████╗██║  ██║
╚═╝     ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝
Gerador de Fichas de Implantação 2.0 · 2025 · Mauricio Luan
""")


def get_dados(headers):
    """
    aqui solicita o id do chamado, o numero de terminais e logo
    em seguida faz o get na API do Tomticket
    """

    ticket_id = input("Digite o ID do chamado: ")
    n_terminais = input("Digite o número de terminais: ")

    response_chamado = requests.get(f"{API_TICKET_URL}{ticket_id}", headers=headers)
    dados_chamado = response_chamado.json()
    conta_empresa_loja = dados_chamado["data"]["customer"]["internal_id"]

    response_cliente = requests.get(f"{API_URL}{conta_empresa_loja}", headers=headers)

    try:
        if response_cliente.status_code == 200 and response_chamado.status_code == 200:
            return response_chamado, response_cliente, n_terminais
        else:
            print(
                f"Retorno da requisição do cliente: {response_cliente.status_code} - {response_cliente.reason}"
            )
            print(
                f"Retorno da requisição do chamado: {response_chamado.status_code} - {response_chamado.reason}"
            )
            return None, None, None
    except Exception as e:
        print(f"Erro ao obter dados: {e}")
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

    return planilha


if __name__ == "__main__":
    while True:
        response_chamado, response_cliente, n_terminais = get_dados(headers)
        if not response_chamado or not response_cliente:
            continue

        planilha = organiza_os_dados(response_chamado, response_cliente, n_terminais)

        # salva tudão
        caminho_base = f"G:\\Drives compartilhados\\FICHAS DE IMPLANTACAO"
        if not os.path.exists(caminho_base):
            caminho_base = os.path.join(os.path.expanduser("~"), "Documents")
            print(f"Pasta base não encontrada. Salvando em: {caminho_base}\n")

        primeira_letra = planilha["Razão Social"][0].upper()
        subpasta_letra = os.path.join(caminho_base, primeira_letra)
        os.makedirs(subpasta_letra, exist_ok=True)
        pasta_razao_social = os.path.join(subpasta_letra, planilha["Razão Social"])
        os.makedirs(pasta_razao_social, exist_ok=True)
        arquivo_excel = os.path.join(pasta_razao_social, f"{planilha['Loja']}.xlsx")
        caminho_imagem = encontrar_imagem("payer.png")

        gerar_planilha_estilizada(planilha, arquivo_excel, caminho_imagem)
        os.startfile(pasta_razao_social) 