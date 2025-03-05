from fastapi import APIRouter
from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from .. import schemas, database, models, hashing
from ..repository import users_rep
from typing import List

get_db = database.get_db

router = APIRouter(
    tags =['user'],
    prefix="/user"
)

@router.post('/', response_model=schemas.Show_user, status_code=status.HTTP_200_OK)
def create_user(request:schemas.User, db :Session = Depends(get_db)):
    return(users_rep.register_user(request,db))
    

@router.get('/', response_model=schemas.Show_user)#show user
def show_user(id:int, response = Response,db :Session = Depends(get_db) ):
   return users_rep.spec_user(id,response,db)