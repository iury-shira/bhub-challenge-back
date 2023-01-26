from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from .. import schemas, models
from fastapi import status, HTTPException
from ..utils import hashing


def get_all(db: Session):
    return db.query(models.User).all()


def get_by_id(id: int, db: Session):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        message = {"detail": f"Message with id {id} not available"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)

    return user


def create(request: schemas.User, db: Session):
    hashed_pwd = hashing.bcrytp(request.password)
    new_user = models.User(name=request.name, email=request.email, password=hashed_pwd)

    try:
        db.add(new_user)
        db.flush()
    except IntegrityError:
        db.rollback()
        message = {"detail": f"A client with same corporate name and/or phone number is already registered"}
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)

    db.commit()
    db.refresh(new_user)
    return new_user
