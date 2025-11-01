from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict

# Initialize FastAPI app
app = FastAPI()

# In-memory storage for users: mapping user ID to user data dict
users_db: Dict[int, Dict] = {}

class User(BaseModel):
    """
    Pydantic model for user data validation.

    Attributes:
    - id: Unique integer identifier for the user.
    - name: Full name of the user.
    - email: Email address of the user.
    """
    id: int
    name: str
    email: str

@app.post("/users", status_code=200)
def create_user(user: User):
    """
    Create a new user entry in the in-memory database.

    Request Body:
    - user: User model with id, name, email.

    Responses:
    - 201: User created successfully.
    - 400: User ID already exists.
    """
    # Check for duplicate ID
    if user.id in users_db:
        # Raise HTTP 400 if ID already taken
        raise HTTPException(status_code=400, detail="User ID already exists.")
    # Store the user data as plain dict
    users_db[user.id] = user.model_dump()
    return {"message": f"User {user.name} created successfully."}

@app.get("/users/{user_id}")
def get_user(user_id: int):
    """
    Retrieve a user's data by their ID.

    Path Parameters:
    - user_id: Integer ID of the user to fetch.

    Responses:
    - 200: Returns the user data.
    - 404: User not found.
    """
    # Attempt to fetch from in-memory DB
    user = users_db.get(user_id)
    if not user:
        # Raise HTTP 404 if missing
        raise HTTPException(status_code=404, detail="User not found.")
    return user

@app.put("/users/{user_id}")
def update_user(user_id: int, updated_user: User):
    """
    Update an existing user's information.

    Path Parameters:
    - user_id: ID of the user to update.
    Request Body:
    - updated_user: Full user model (id must match or ignored).

    Responses:
    - 200: User updated successfully.
    - 404: User not found.
    """
    if user_id not in users_db:
        # Cannot update non-existent user
        raise HTTPException(status_code=404, detail="User not found.")
    # Overwrite stored record with new data
    users_db[user_id] = updated_user.model_dump()
    return {"message": f"User {updated_user.name} updated successfully."}

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    """
    Delete a user from the in-memory database.

    Path Parameters:
    - user_id: ID of the user to delete.

    Responses:
    - 200: User deleted successfully.
    - 404: User not found.
    """
    if user_id not in users_db:
        # Cannot delete non-existent user
        raise HTTPException(status_code=404, detail="User not found.")
    # Remove user entry
    del users_db[user_id]
    return {"message": f"User {user_id} deleted successfully."}