# Exemplo de resposta da API TomTicket.
# As classes a seguir representam o schema Ticket que mapeia a resposta da API.
# {
#   "data": {
#     "protocol": 30049,
#     "customer": {
#       "internal_id": "001693-009816-0001",
#     },
# }

from typing import Optional
from pydantic import BaseModel


class CustomerData(BaseModel):
    internal_id: str


class DataTicket(BaseModel):
    protocol: int
    customer: CustomerData


class Ticket(BaseModel):
    data: DataTicket
    success: bool


# Exemplo de resposta da API TomTicket.
# As classes a seguir representam o schema Customer que mapeia a resposta da API.

#   "data": [
#     {
#       "name": "HAMBURGUERIA LTDA",
#       "custom_fields": [
#         {
#           "name": "Nome Fantasia",
#           "value": "HAMBURGUERIA JUAZEIRO DO NORTE"
#         },
#         {
#           "name": "CNPJ",
#           "value": "99900011100120"
#         },
#       ]


class CustomFields(BaseModel):
    name: str
    value: Optional[str] = None


class Data(BaseModel):
    name: str
    internal_id: str
    custom_fields: list[CustomFields]


class Customer(BaseModel):
    data: list[Data]
    success: bool
