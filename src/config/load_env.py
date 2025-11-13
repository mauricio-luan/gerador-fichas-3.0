import os
import sys
from pathlib import Path
from dotenv import load_dotenv


def load_env():
    if getattr(sys, "frozen", False):
        app_path = Path(sys.executable).parent
        print(f"executavel: {app_path}")
    else:
        app_path = Path(__file__).parent.parent.parent
        print(f"dev: {app_path}")

    env_path = app_path / ".env"

    if env_path.exists():
        load_dotenv(dotenv_path=env_path)

        ticket_url = os.getenv("API_TICKET_URL")
        customer_url = os.getenv("API_CUSTOMER_URL")
        token = os.getenv("API_TOKEN")

        if not all([ticket_url, customer_url, token]):
            raise ValueError("Uma ou mais variaveis de ambiente estao faltando.")

        header = {"Authorization": f"Bearer {token}"}

        return ticket_url, customer_url, header
    else:
        raise ValueError(".env não encontrado.")
