from pydantic import BaseModel
import uvicorn

from fastapi import FastAPI

from typing import Optional

app = FastAPI()

@app.get('/blog')
def index(limit = 10, published: bool = True, sort: Optional[str] = None):
    if published:
        return {'data': f'{limit} published blog db!'}
    else:
        return {'data': f'{limit} blog db!'}

@app.get('/blog/unpublished')
def unpublished():
    return {
        'data': 'All unpublished blogs!'
    }

@app.get('/blog/{id}')
def show(id: int):
    return {'data': id}

@app.get('/blog/{id}/comments')
def comments(id: int, limit=10):
    return {
        'data': {1, 2},
    }

class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool]

@app.post('/blog')
def create_blog(blog: Blog):
    return blog

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=9000)