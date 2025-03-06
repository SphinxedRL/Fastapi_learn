from fastapi import APIRouter, Depends, HTTPException,status
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from .. import schemas, database, models
from ..hashing import Hash
from . import token
get_db=database.get_db

router = APIRouter(tags=["authentication"], prefix='/auth')
@router.post('/')
def login(request:schemas.Login,db:Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.email==request.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Invalid login credentials"
        )
    if not Hash.verify(user.password,request.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Wrong password"
        )
    #access_token_expires = timedelta(minutes=token.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = token.create_access_token(
        data={"sub": user.email}#, expires_delta=access_token_expires
    )
    return schemas.Token(access_token=access_token, token_type="bearer")