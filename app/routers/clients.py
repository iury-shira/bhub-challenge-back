from typing import List
from .. import schemas
from fastapi import APIRouter, Depends

from datetime import datetime

# temp_in_memory_clients_db
temps = [
    {'corporate_name': 'josuke', 'phone_number': '12345', 'declared_billing': 1000, 'created_at': datetime.now(), 'id': 1, 'password': '123'},
    {'corporate_name': 'jotaro', 'phone_number': '67890', 'declared_billing': 2000, 'created_at': datetime.now(), 'id': 2, 'password': '123'}
]

router = APIRouter(
    prefix='/client',
    tags=['Clients']
)

@router.get('/', response_model=List[schemas.ClientOut])
def get_clients():
    return temps

@router.get('/{id}', response_model=schemas.ClientOut)
def get_client_by_id(id: int):
    client = {'corporate_name': '', 'phone_number': '', 'declared_billing': 0, 'created_at': datetime.now(), 'id': 0}
    for temp in temps:
        if temp['id'] == id:
            client = temp
    return client


@router.post('/', response_model=schemas.ClientOut)
def create_client(request: schemas.ClientCreate):
    client = {}
    client['corporate_name'] = request.corporate_name
    client['phone_number'] = request.phone_number
    client['declared_billing'] = request.declared_billing
    client['created_at'] = datetime.now()
    client['id'] = len(temps) + 1
    client['password'] = request.password
    temps.append(client)
    return client
