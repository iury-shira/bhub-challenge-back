from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class BankDataCreate(BaseModel):
    agency: str
    account: str
    bank: str
    owner_id: int


class BankDataOut(BaseModel):
    id: int
    agency: str
    account: str
    bank: str
    owner_id: int

    class Config:
        orm_mode = True


class ClientOut(BaseModel):
    id: int
    corporate_name: str
    phone_number: str
    declared_billing: int
    created_at: datetime

    class Config:
        orm_mode = True


class ClientOutWithBankData(ClientOut):
    bank_data: list[BankDataOut] = []


class ClientCreate(BaseModel):
    corporate_name: str
    phone_number: str
    declared_billing: int


class BankDataOutWithOwnerData(BankDataOut):
    owner: ClientOut
