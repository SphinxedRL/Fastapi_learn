from sqlalchemy.orm import Session
from fastapi import HTTPException,status
from ..import models
def get_all(db: Session):
    blogs= db.query(models.Blog).all()
    return blogs

def create_blog(request, db:Session):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

def destroy_blog(id, db:Session):
    db.query(models.Blog).filter(models.Blog.id==id).delete(synchronize_session=False)
    db.commit()
    return{'deletion successful'}

def blog_update(id, request, db):
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
def spec_blog(id, response,db):
    blog = db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blog:
        response.status_code=status.HTTP_404_NOT_FOUND
        return {'detail':"This blog with the id {id} does not exist."}
    return blog