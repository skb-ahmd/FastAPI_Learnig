from typing import Optional, Union

from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
    title:str
    content:str
    published:bool = True
    rating: Optional[int]=None

    

@app.get("/")
def root():
    return {"Message": "Hello World"}


@app.get("/posts")
def read_item():
    return {"data":"This is your posts"}


@app.post("/createposts")
def create_post(post:Post):
    print(post.model_dump())
    return {"New Post": post}
