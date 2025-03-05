from fastapi import APIRouter
from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from .. import schemas, database, models, hashing
from typing import List

get_db = database.get_db

router = APIRouter()

@router.post('/user', response_model=schemas.Show_user, status_code=status.HTTP_200_OK, tags=['user'])
def create_user(request:schemas.User, db :Session = Depends(get_db)):
    
    new_user = models.User(name =request.name, email=request.email, password=hashing.Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/user', response_model=schemas.Show_user, tags=['user'])#show user
def show_user(id:int, response = Response,db :Session = Depends(get_db) ):
    user = db.query(models.User).filter(models.User.id==id).first()
    if not user:
        response.status_code=status.HTTP_404_NOT_FOUND
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"This user with the id {id} does not exist.")
    return user