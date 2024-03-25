from typing import List

from fastapi import FastAPI, Depends, status, Response, HTTPException

from sqlalchemy.orm import Session


from .database import engine, SessionLocal
from . import schemas, models

# Hash
from .hashing import Hash

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
@app.post('/blog', status_code=status.HTTP_201_CREATED, tags=['blogs'])
def create(blog: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(
        title=blog.title,
        body=blog.body,
        user_id=1
    )

    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    return new_blog

@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['blogs'])
def destroy(id: str, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Bu id={id} bilan blog topilmadi!")

    blog.delete(synchronize_session=False)

    db.commit()

    return 'done'

@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED, tags=['blogs'])
def update(id, blog: schemas.Blog, db: Session = Depends(get_db)):
    update_blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not update_blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Bu id={id} bilan blog topilmadi!")
    update_blog.update(
        {
            'title': blog.title,
            'body': blog.body
        }
    )
    db.commit()

    return 'Updated!'

@app.get('/blog', status_code=status.HTTP_200_OK, response_model=List[schemas.ShowBlog], tags=['blogs'])
def all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.get('/blog/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog, tags=['blogs'])
def show(id: str, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()

    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{id} id bilan blog topilmadi!"
        )

    return blog

# User ------

@app.post('/user', response_model=schemas.ShowUser, tags=['users'])
def create_user(user: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(
        name=user.name,
        email=user.email,
        password=Hash.bcrypt(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get('/user/{id}', response_model=schemas.ShowUser, tags=['users'])
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{id} li user mavjud emas!")

    return user

