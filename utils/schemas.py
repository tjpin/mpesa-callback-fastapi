from pydantic import BaseModel
from typing import Dict


class User(BaseModel):
    first_name: str
    last_name: str
    phone_number: int
    email: str
    password: str


# class PublicUser(User):
#     first_name: str
#     last_name: str
#     phone_number: int
#     email: str


class Transaction(BaseModel):
    Amount: str
    MpesaReceiptNumber: str
    TransactionDate: str
    PhoneNumber: int

    class Config:
        orm_mode = True
    
