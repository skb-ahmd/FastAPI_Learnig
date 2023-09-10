from typing import Union

from fastapi import FastAPI
from fastapi.params import Body

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.post("/createposts")
def create_post(payload: dict = Body(...)):
    # print(payload)
    return {"New Post": f"title {payload['title']} Contetnt : {payload['content']}"}
