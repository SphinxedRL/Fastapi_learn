from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session
from .. import schemas, database, models
from ..hashing import Hash
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
    #assign JWD token
    return user
