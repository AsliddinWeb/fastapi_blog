from fastapi import FastAPI

app = FastAPI()

@app.get('/blog')
def index():
    return {'data': 'Blog list!'}

@app.get('/blog/unpublished')
def unpublished():
    return {
        'data': 'All unpublished blogs!'
    }

@app.get('/blog/{id}')
def show(id: int):
    return {'data': id}

@app.get('/blog/{id}/comments')
def comments(id: int):
    return {
        'data': {1, 2},
    }