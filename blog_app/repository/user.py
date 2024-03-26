from fastapi import status, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import schemas, database, models, hashing

get_db = database.get_db

def create_user(user: schemas.User, db: Session = Depends(get_db)):
    get_user = db.query(models.User).filter(models.User.email == user.email).first()
    if get_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"{get_user.email} li user mavjud!")
    new_user = models.User(
        name=user.name,
        email=user.email,
        password=hashing.Hash.bcrypt(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{id} li user mavjud emas!")

    return user