from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ClientOut(BaseModel):
    id: int
    corporate_name: str
    phone_number: str
    declared_billing: int
    created_at: datetime

    class Config:
        orm_mode = True


class ClientCreate(BaseModel):
    corporate_name: str
    phone_number: str
    declared_billing: int
    password: str
