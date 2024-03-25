from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import schemas, database

from ..repository import user as user_view

router = APIRouter(
    prefix="/user",
    tags=['Users']
)

get_db = database.get_db

@router.post('/', response_model=schemas.ShowUserBlogs)
def create_user(user: schemas.User, db: Session = Depends(get_db)):
    return user_view.create_user(user, db)

@router.get('/{id}', response_model=schemas.ShowUserBlogs)
def get_user(id: int, db: Session = Depends(get_db)):
    return user_view.get_user(id, db)

