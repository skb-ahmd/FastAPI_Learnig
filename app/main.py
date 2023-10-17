from random import randrange
from typing import Optional, Union

from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models
from . database import engine, get_db
# test 1

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    # rating: Optional[int] = None


while True:

    try:
        conn = psycopg2.connect(host="localhost", database="fastapi",
                                user="postgres", password="open", cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was succesful")
        break
    except Exception as error:
        print("Connecting to database failed")
        print(f"error was {error}")
        time.sleep(2)


my_posts = [{"title": "Title of post 1", "content": "Content of post 1", "id": 1}, {
    "title": "Title of post 1", "content": "Content of post 1", "id": 2}]


def find_post(id):
    for post in my_posts:
        if post["id"] == id:
            return post


def find_index_post(id):
    for index, post in enumerate(my_posts):
        if post['id'] == id:
            return index


@app.get("/")
def root():
    return {"Message": "Hello Qorld"}


@app.get("/sqlalchemy")
def test(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}


@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post, db: Session = Depends(get_db)):
    # cursor.execute(""" Insert into posts (title,content,published) Values (%s,%s,%s) Returning * """,
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"New Post": new_post}


@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    cursor.execute(""" Select * from posts where id=%s""", (str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} is not exist")
    return {"post_details": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute(
        """ Delete from posts where id=%s returning *""", (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"no post with id {id}")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_post(id: int, post: Post):
    cursor.execute(""" Update posts set title = %s ,content = %s,published = %s where id = %s  Returning * """,
                   (post.title, post.content, post.published, id))
    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"no post with id {id}")

    return {"data": updated_post}
