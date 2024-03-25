from fastapi import Response, status, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import schemas, database, models

get_db = database.get_db

def get_all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

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

def destroy(id: str, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Bu id={id} bilan blog topilmadi!")

    blog.delete(synchronize_session=False)

    db.commit()

    return 'done'

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

def show(id: str, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()

    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{id} id bilan blog topilmadi!"
        )

    return blog