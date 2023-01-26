from typing import List
from .. import schemas, database
from ..authentication import oauth2
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from ..repository import clients as clients_repository

router = APIRouter(
    prefix='/client',
    tags=['Clients']
)

get_db = database.get_db

@router.get('/', response_model=List[schemas.ClientOut])
def get_clients(db: Session = Depends(get_db), from_date: str | None = None, declared_billing: int | None = None, current_user: schemas.User = Depends(oauth2.get_current_user)):
    return clients_repository.get_all(db, from_date, declared_billing)


@router.get('/{id}', response_model=schemas.ClientOutWithBankData)
def get_client_by_id(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return clients_repository.get_by_id(id, db)


@router.get('/corporate_name/{corporate_name}', response_model=schemas.ClientOutWithBankData)
def get_client_by_id(corporate_name: str, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return clients_repository.get_by_corporate_name(corporate_name, db)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.ClientOut)
def create_client(request: schemas.ClientCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return clients_repository.create(request, db)


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=schemas.ClientOut)
def update_client(id: int, request: schemas.ClientCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return clients_repository.update(id, request, db)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_client(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    clients_repository.delete(id, db)
    return