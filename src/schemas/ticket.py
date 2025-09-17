from pydantic import BaseModel


class Customer(BaseModel):
    internal_id: str


class Data(BaseModel):
    protocol: int
    customer: Customer


class Ticket(BaseModel):
    data: Data
    success: bool
