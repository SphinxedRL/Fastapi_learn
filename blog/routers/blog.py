from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.orm import Session
from .. import schemas, database, models
from typing import List
from ..repository import blog_rep

router = APIRouter(#prefix & tags added
    tags=['blog'],
    prefix="/blog")

@router.get('/', response_model=List[schemas.Show_blog]) #change to return only title. If entire thing req, remove response_model
def all(db :Session = Depends(database.get_db)):
    return blog_rep.get_all(db)

@router.post('/', status_code=status.HTTP_201_CREATED)
def create(request:schemas.Blog, db :Session = Depends(database.get_db)):
    return blog_rep.create_blog(request, db)
    

@router.get('/{id}',status_code=status.HTTP_200_OK, response_model=schemas.Show_blog)
def get_spec(id,response :Response, db :Session = Depends(database.get_db)):
    return blog_rep.spec_blog(id, response,db)

@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def destroy(id, db :Session = Depends(database.get_db)):
    return blog_rep.destroy_blog(id, db)

@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id, request:schemas.Blog, db :Session = Depends(database.get_db)):
   return blog_rep.blog_update(id,request,db)