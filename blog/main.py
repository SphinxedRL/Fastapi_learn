from typing import List
from fastapi import FastAPI , Depends, status, Response, HTTPException
from . import schemas, models, hashing
from .database import engine, Sessionlocal
from sqlalchemy.orm import Session


app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/check')
def give():
    return{"text": "Helloworld"}


@app.post('/blog', status_code=status.HTTP_201_CREATED, tags=['blog'])
def create(request:schemas.Blog, db :Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.get('/blog', response_model=List[schemas.Show_blog], tags=['blog']) #change to return only title. If entire thing req, remove response_model
def all(db :Session = Depends(get_db)):
    blogs= db.query(models.Blog).all()
    return blogs

@app.get('/blog/{id}',status_code=status.HTTP_200_OK, response_model=schemas.Show_blog, tags=['blog'])
def get_spec(id,response :Response, db :Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blog:
        response.status_code=status.HTTP_404_NOT_FOUND
        return {'detail':"This blog with the id {id} does not exist."}
    return blog

@app.delete('/blog/{id}',status_code=status.HTTP_204_NO_CONTENT, tags=['blog'])
def destroy(id, db :Session = Depends(get_db)):
    db.query(models.Blog).filter(models.Blog.id==id).delete(synchronize_session=False)
    db.commit()
    return{'deletion successful'}

@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED, tags=['blog'])
def update(id, request:schemas.Blog, db :Session = Depends(get_db)):
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


@app.post('/user', response_model=schemas.Show_user, status_code=status.HTTP_200_OK, tags=['user'])
def create_user(request:schemas.User, db :Session = Depends(get_db)):
    
    new_user = models.User(name =request.name, email=request.email, password=hashing.Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get('/user', response_model=schemas.Show_user, tags=['user'])#show user
def show_user(id:int, response = Response,db :Session = Depends(get_db) ):
    user = db.query(models.User).filter(models.User.id==id).first()
    if not user:
        response.status_code=status.HTTP_404_NOT_FOUND
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"This user with the id {id} does not exist.")
    return user