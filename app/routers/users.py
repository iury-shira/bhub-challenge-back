from typing import List
from .. import schemas
from fastapi import APIRouter, Depends

# temp_in_memory_users_db
temps = [
    {'name': 'josuke', 'email': 'josuke@bhub.com', 'id': 1},
    {'name': 'jotaro', 'email': 'jotaro@bhub.com', 'id': 2}
]

router = APIRouter(
    prefix='/user',
    tags=['Users']
)

@router.get('/', response_model=List[schemas.ShowUser])
def get_users():
    return temps

@router.get('/{id}', response_model=schemas.ShowUser)
def get_user_by_id(id: int):
    user = {'name': '', 'email': ''}
    for temp in temps:
        if temp['id'] == id:
            user = temp
    return user


@router.post('/', response_model=schemas.ShowUser)
def create_user(request: schemas.User):
    user = {}
    user['name'] = request.name
    user['email'] = request.email
    temps.append(user)
    return user