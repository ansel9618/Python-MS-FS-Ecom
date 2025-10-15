from fastapi import FastAPI,Query
from typing import Optional
main = FastAPI()

@main.get('/say_hello_guys')
def say_hello():
    return {'message':'Hello, world! This is your First Microservice'}


@main.get('/speak/{name}')
def say_hello_to(name: str):
    return {'message':f'Hello, {name}! This is your First Microservice'}

@main.get('/add_numbers/{num1}/{num2}')
def add_numbers(num1: int, num2:int):
    return {'result2': num1 + num2}

@main.get('/say_hello')
def say_hello_everyone(name:str= Query('Stranger', description="This is a eg of how to use optional query parameters")):
    return {'message' : f'Hello {name}'}
 