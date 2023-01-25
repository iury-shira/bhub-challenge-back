from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from .. import schemas, models
from fastapi import status, HTTPException
from . import bankdata as bankdata_repository


def get_all(db: Session, from_date: str | None, declared_billing: int | None):
    client_query = db.query(models.Client)
    if from_date:
        client_query = client_query.filter(models.Client.created_at >= from_date)
    if declared_billing:
        client_query = client_query.filter(models.Client.declared_billing >= declared_billing)
    return client_query.all()


def get_by_id(id: int, db: Session):
    client = db.query(models.Client).filter(models.Client.id == id).first()

    if not client:
        message = {"detail": f"Client with id {id} not available"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)
    return client


def get_by_corporate_name(corporate_name: str, db: Session):
    client = db.query(models.Client).filter(models.Client.corporate_name == corporate_name).first()

    if not client:
        message = {"detail": f"Client with corporate_name {corporate_name} not available"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)
    return client


def create(request: schemas.ClientCreate, db: Session):
    new_client = models.Client(
        corporate_name=request.corporate_name,
        phone_number = request.phone_number,
        declared_billing = request.declared_billing,
        )

    try:
        db.add(new_client)
        db.flush()
    except IntegrityError:
        db.rollback()
        message = {"detail": f"A client with same corporate name and/or phone number is already registered"}
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)

    db.commit()
    db.refresh(new_client)
    return new_client

def update(id: int, request: schemas.ClientCreate, db: Session):
    client = db.query(models.Client).filter(models.Client.id == id)

    if not client.first():
        message = {"detail": f"Client with id {id} not available"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)

    try:
        client.update(request.dict())
        db.flush()
    except IntegrityError:
        db.rollback()
        message = {"detail": f"A client with same corporate name and/or phone number is already registered"}
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)

    db.commit()
    return client.first()


def delete(id: int, db: Session):
    client = db.query(models.Client).filter(models.Client.id == id)

    if not client.first():
        message = {"detail": f"Message with id {id} not available"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)

    client.delete(synchronize_session=False)
    bankdata_repository.delete_by_owner_id(id, db)
    db.commit()
    return