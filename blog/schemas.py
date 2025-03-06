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

class User1(BaseModel):
    name: str
    email: str
    class Config:
         from_attributes = True

class Show_user(BaseModel):
    name: str
    email: str
    blogs: List[Blog] =[]
    class Config:
         from_attributes = True


class Show_blog(BaseModel): #used to display response model as we want instead of all parameters in the schema stored in db
    title:str
    body: str
    creator: User1
    class Config:
        from_attributes = True

class Login(BaseModel):#for login credentials
    username: str
    password: str
    class Config:
        from_attributes = True
