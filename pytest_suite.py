import requests

BASE_URL = "http://127.0.0.1:8000"

def test_create_user_1():
    user_data = {"id":1,"name":"Alice","email":"alice@example.com"}
    resp = requests.post(f'{BASE_URL}/users',json=user_data)
    assert resp.status_code == 200
    assert "User Alice created successfully" in resp.text

def test_create_user_2():
    user_data = {"id":2,"name":"Bob","email":"bob@example.com"}
    resp = requests.post(f'{BASE_URL}/users',json=user_data)
    assert resp.status_code == 200
    assert "User Bob created successfully" in resp.text

def test_get_user_1():
    resp = requests.get(f'{BASE_URL}/users/1')
    assert resp.status_code == 200
    data = resp.json()
    assert data['name'] == "Aice"

def test_delete_user_2():
    resp = requests.delete(f"{BASE_URL}/users/2")
    assert resp.status_code == 200
    assert "User 2 deleted successfully." in resp.text

def test_get_user_2_should_be_404():
    """
    Test retrieving a deleted or non-existent user (ID=2).

    - Sends GET to /users/2 after deletion.
    - Expects status code 404 (Not Found).
    """
    resp = requests.get(f"{BASE_URL}/users/2")
    # After deletion, the user should no longer exist
    assert resp.status_code == 404