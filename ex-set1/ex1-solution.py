from fastapi import FastAPI

main = FastAPI()

count=0

@main.get('/count')
def get_count():
    return {"count":count}

@main.get('/')
@main.get('/speak')
def say_hello():
    global count
    count +=1
    return {'message': 'Hello, world! This is your First Microservice'}
