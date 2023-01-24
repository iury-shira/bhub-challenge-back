from typing import List
from sqlalchemy.orm import Session
from .. import schemas, models
from fastapi import status, HTTPException


def get_all(db: Session):
    return db.query(models.Client).all()


def get_by_id(id: int, db: Session):
    client = db.query(models.Client).filter(models.Client.id == id).first()

    if not client:
        message = {"detail": f"Client with id {id} not available"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)

    return client


def create(request: schemas.ClientCreate, db: Session):
    new_client = models.Client(
        corporate_name=request.corporate_name,
        phone_number = request.phone_number,
        declared_billing = request.declared_billing,
        password = request.password
        )
    db.add(new_client)
    db.commit()
    db.refresh(new_client)
    return new_client