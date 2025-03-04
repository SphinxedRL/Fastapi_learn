#importing 
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from typing import Optional


app =  FastAPI()
@app.get("/blog")
def index(limit = 10, published:bool = True):
    if published:
        return {'data':f'{limit} published blogs from database'}
    else:
        return{'data':f'{limit}blogs from database'}


@app.get("/blog/unpublished")
def unpublished():
    return {'data': {"all unpublished blogs"}}
 
@app.get("/blog/{id}")
def about(id:int):
    return {"about":id}

class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool]

@app.post("/blog")
def create_blog(request:Blog):
    # return request
    return {'data': f"Blog created with title as {request.title}"}

# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=8000)