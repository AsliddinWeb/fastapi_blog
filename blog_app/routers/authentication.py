from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from fastapi.security import OAuth2PasswordRequestForm

from .. import schemas, database, models, hashing, token

router = APIRouter(
    tags=['Authentication']
)

@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends( ), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Bu id={id} bilan user topilmadi!")

    if not hashing.Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Parol noto'g'ri")

    access_token = token.create_access_token(
        data={"sub": user.email}
    )
    return schemas.Token(access_token=access_token, token_type="bearer")