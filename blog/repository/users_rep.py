from sqlalchemy.orm import Session
from fastapi import HTTPException,status
from ..import models, hashing
def register_user(request,db):
    new_user = models.User(name =request.name, email=request.email, password=hashing.Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def spec_user(id, response, db):
    user = db.query(models.User).filter(models.User.id==id).first()
    if not user:
        response.status_code=status.HTTP_404_NOT_FOUND
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"This user with the id {id} does not exist.")
    return user