from random import randrange
from typing import Optional, Union

from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


my_posts = [{"title": "Title of post 1", "content": "Content of post 1", "id": 1}, {
    "title": "Title of post 1", "content": "Content of post 1", "id": 2}]


def find_post(id):
    for post in my_posts:
        if post["id"] == id:
            return post


@app.get("/")
def root():
    return {"Message": "Hello Qorld"}


@app.get("/posts")
def get_posts():
    return {"data": my_posts}


@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 9999999)
    my_posts.append(post_dict)
    return {"New Post": post_dict}


@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} is not exist")
        # response.status_code =status.HTTP_404_NOT_FOUND
        # return {"message":f"post with id {id} is not exist"}
    return {"post_details": post}
