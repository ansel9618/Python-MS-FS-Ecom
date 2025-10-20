from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict

# Initialize FastAPI app
app = FastAPI()

# In-memory storage for users: mapping user ID to user data dict
users_db: Dict[int, Dict] = {}

#user model
class User(BaseModel):
    id: int
    name: str
    email: str

#create user
@app.post("/users")
def create_user(user: User):
    if user.id in users_db:
        raise HTTPException(status_code=400, detail="User ID already exists. ")
    users_db[user.id] = user.model_dump()
    return {"message":f"user {user.name} created successfully"}

#get a user
@app.post("/users/{user_id}")
def get_user(user_id: int):
    user = users_db.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    return user

#update a user
@app.post("/users/{user_id}")
def create_user(user_id: int, updated_user: User):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found.")
    users_db[user_id] = updated_user.model_dump()
    return {"message":f"User {updated_user.name} updated successfully"}

#Delete a  user
@app.post("/users/{user_id}")
def create_user(user_id:int ):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    del users_db[user_id]
    return {"message":f"User {user_id} deleted successfully"}

