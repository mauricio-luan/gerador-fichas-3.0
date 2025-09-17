import os
from dotenv import load_dotenv

# from logic.config_log import configura_logger

# log = configura_logger("gerador-fichas-3.0.load_env")


def load_env():
    # log.debug("Carregando variaveis de ambiente...")
    load_dotenv()

    api_url = os.getenv("API_URL")
    api_ticket_url = os.getenv("API_TICKET_URL")
    api_token = os.getenv("API_TOKEN")

    if not all([api_url, api_ticket_url, api_token]):
        # log.error("Erro ao carregar variaveis de ambiente")
        raise ValueError("Uma ou mais variaveis de ambiente estao faltando.")

    # log.debug("Variaveis de ambiente carregadas.")
    headers = {"Authorization": f"Bearer {api_token}"}

    return api_url, api_ticket_url, headers
