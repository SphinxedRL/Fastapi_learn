from fastapi import FastAPI 
from . import  models
from .database import engine
from .routers import blog, user


app = FastAPI()
app.include_router(blog.router)
app.include_router(user.router)

models.Base.metadata.create_all(bind=engine)

# def get_db():
#     db = Sessionlocal()
#     try:
#         yield db
#     finally:
#         db.close()

@app.get('/check')
def give():
    return{"text": "Helloworld"}




# @app.get('/blog', response_model=List[schemas.Show_blog], tags=['blog']) #change to return only title. If entire thing req, remove response_model
# def all(db :Session = Depends(get_db)):
#     blogs= db.query(models.Blog).all()
#     return blogs




