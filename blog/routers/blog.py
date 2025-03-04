from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from .. import schemas, database, models
from typing import List

router = APIRouter(#prefix & tags added
    tags=['blog'],
    prefix="/blog")

@router.get('/', response_model=List[schemas.Show_blog]) #change to return only title. If entire thing req, remove response_model
def all(db :Session = Depends(database.get_db)):
    blogs= db.query(models.Blog).all()
    return blogs

@router.post('/', status_code=status.HTTP_201_CREATED)
def create(request:schemas.Blog, db :Session = Depends(database.get_db)):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@router.get('/{id}',status_code=status.HTTP_200_OK, response_model=schemas.Show_blog)
def get_spec(id,response :Response, db :Session = Depends(database.get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blog:
        response.status_code=status.HTTP_404_NOT_FOUND
        return {'detail':"This blog with the id {id} does not exist."}
    return blog

@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def destroy(id, db :Session = Depends(database.get_db)):
    db.query(models.Blog).filter(models.Blog.id==id).delete(synchronize_session=False)
    db.commit()
    return{'deletion successful'}

@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id, request:schemas.Blog, db :Session = Depends(database.get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id==id)
    point = blog.first()
    if not point:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Blog with id {id} does not exist"
        )
    blog.update(request.model_dump())
    db.commit()
    return {'ok, updated'}