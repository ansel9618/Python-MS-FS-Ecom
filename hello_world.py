from fastapi import FastAPI

main = FastAPI()

@main.get('/say_hello')
def say_hello():
    return {'message':'Hello, world! This is your First Microservice'}
