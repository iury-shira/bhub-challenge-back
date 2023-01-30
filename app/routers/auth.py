

from .. import database, models
from ..utils import token, hashing
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

router = APIRouter(
    prefix='/login',
    tags=['Authentication']
)

get_db = database.get_db


@router.post('/')
def get_user(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    print(request)

    user = db.query(models.User).filter(models.User.email == request.username).first()

    if not user:
        message = {"detail": f"User with username {request.username} not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)
    elif not hashing.match_pwd(request.password, user.password):
        message = {"detail": f"Incorrect password"}
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=message)

    access_token = token.create_access_token(data={"sub": user.email + ' ' + str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}
