from pydantic import BaseModel
from typing import List

class Blog(BaseModel):
    title: str
    body:str
    class Config:
         from_attributes = True


class User(BaseModel):
    name: str
    email: str
    password: str


class Show_user(BaseModel):
    name: str
    email: str
    blogs: List[Blog] =[]
    class Config:
         from_attributes = True


class Show_blog(BaseModel): #used to display response model as we want instead of all parameters in the schema stored in db
    title:str
    body: str
    creator: Show_user
    class Config:
        from_attributes = True