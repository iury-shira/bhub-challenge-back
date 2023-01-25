from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from . import clients as clients_repository
from .. import schemas, models
from fastapi import status, HTTPException


def get_all(db: Session, bank: str):
    if bank:
        return db.query(models.BankData).filter(models.BankData.bank == bank).all()
    return db.query(models.BankData).all()


def get_by_id(id: int, db: Session):
    bank_data = db.query(models.BankData).filter(models.BankData.id == id).first()

    if not bank_data:
        message = {"detail": f"Bank data with id {id} not available"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)

    return bank_data


def create(request: schemas.BankDataCreate, db: Session):
    try:
        clients_repository.get_by_id(request.owner_id, db)
        new_bank_data = models.BankData(agency=request.agency, account=request.account, bank = request.bank, owner_id=request.owner_id)
        db.add(new_bank_data)
        db.flush()
    except HTTPException as exc:
        if exc.status_code == status.HTTP_404_NOT_FOUND:
            message = {"detail": f"The client {request.owner_id} is not available"}
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)
    except IntegrityError:
        db.rollback()
        message = {"detail": f"A bank account with same account number is already registered"}
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)

    db.commit()
    db.refresh(new_bank_data)
    return new_bank_data


def update(id: int, request: schemas.BankDataCreate, db: Session):
    bank_data = db.query(models.BankData).filter(models.BankData.id == id)

    if not bank_data.first():
        message = {"detail": f"Bank data with id {id} not available"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)

    try:
        bank_data.update(request.dict())
        db.flush()
    except IntegrityError:
        db.rollback()
        message = {"detail": f"A bank account with same account number is already registered"}
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)

    db.commit()
    return bank_data.first()


def delete(id: int, db: Session):
    bank_data = db.query(models.BankData).filter(models.BankData.id == id)

    if not bank_data.first():
        message = {"detail": f"Bank data with id {id} not available"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)

    bank_data.delete(synchronize_session=False)
    db.commit()
    return

# The method below is necessary just when using SQLite dbs, where CASCADE deletes are not enalbled by default
def delete_by_owner_id(owner_id: int, db: Session):
    db.query(models.BankData).filter(models.BankData.owner_id == owner_id).delete(synchronize_session=False)
    # db.commit()
    return
    