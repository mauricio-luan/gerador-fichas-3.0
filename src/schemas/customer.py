from pydantic import BaseModel
from typing import Optional


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
