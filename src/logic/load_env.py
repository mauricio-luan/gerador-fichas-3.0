import os
from dotenv import load_dotenv

# from logic.config_log import configura_logger

# log = configura_logger("gerador-fichas-3.0.load_env")


def load_env():
    # log.debug("Carregando variaveis de ambiente...")
    load_dotenv()

    ticket_url = os.getenv("API_TICKET_URL")
    customer_url = os.getenv("API_CUSTOMER_URL")
    token = os.getenv("API_TOKEN")

    if not all([ticket_url, customer_url, token]):
        # log.error("Erro ao carregar variaveis de ambiente")
        raise ValueError("Uma ou mais variaveis de ambiente estao faltando.")

    # log.debug("Variaveis de ambiente carregadas.")
    header = {"Authorization": f"Bearer {token}"}

    return ticket_url, customer_url, header
