from typing import Optional
from pydantic import BaseModel


class Ficha(BaseModel):
    chamado: str
    nome_fantasia: str
    razao_social: str
    cnpj: str
    endereco: Optional[str] = None
    bairro: Optional[str] = None
    cidade: Optional[str] = None
    contato: str
    telefone: Optional[str] = None
    email: str
    account: str
    company: str
    store: str
    token: str
    servico_cartao: Optional[str] = None
