import sys
sys.path.insert(0, 'C:/Users/16175/Documents/GitHub/Core_Platform_Phase2.1')

import time
def test_register_user(client):
    username = f"testuser{int(time.time())}"  # Append a timestamp to the username
    response = client.post("/register", json={"username": username, "password": "testpass"})
    print(response.json())
    assert response.status_code == 200

def test_login_user(client):
    response = client.post("/login", json={"username": "testuser", "password": "testpass"})
    assert response.status_code == 200