from typing import List
from .. import schemas, database
from ..authentication import oauth2
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from ..repository import bankdata as bank_data_repository

router = APIRouter(
    prefix='/bankdata',
    tags=['BankData']
)

get_db = database.get_db


@router.get('/', response_model=List[schemas.BankDataOut])
def get_bank_data(db: Session = Depends(get_db), bank: str | None = None, current_user: schemas.User = Depends(oauth2.get_current_user)):
    return bank_data_repository.get_all(db, bank)


@router.get('/{id}', response_model=schemas.BankDataOutWithOwnerData)
def get_bank_data_by_id(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return bank_data_repository.get_by_id(id, db)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.BankDataOut)
def create_bank_data(request: schemas.BankDataCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return bank_data_repository.create(request, db)


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=schemas.BankDataOut)
def update_bank_data(id: int, request: schemas.BankDataCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return bank_data_repository.update(id, request, db)


@router.delete('/{id}', status_code=status.HTTP_202_ACCEPTED)
def delete_bank_data(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    bank_data_repository.delete(id, db)
    return