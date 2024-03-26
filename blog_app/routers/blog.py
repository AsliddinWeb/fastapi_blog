from fastapi import APIRouter, status, Depends, Response
from sqlalchemy.orm import Session
from typing import List

from .. import schemas, database, oauth2

from ..repository import blog as blog_view

router = APIRouter(
    prefix="/blog",
    tags=['Blogs']
)

get_db = database.get_db

@router.get('/', status_code=status.HTTP_200_OK, response_model=List[schemas.ShowBlog])
def all(db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blog_view.get_all(db)

@router.post('/', status_code=status.HTTP_201_CREATED)
def create(blog: schemas.Blog, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blog_view.create(blog,current_user, db)

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id: str, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blog_view.destroy(id, db)

@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id, blog: schemas.Blog, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blog_view.update(id, blog, db)

@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog)
def show(id: str, response: Response, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blog_view.show(id, response, db)
