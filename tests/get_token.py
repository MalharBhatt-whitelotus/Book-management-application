async def get_token(client):
    payload = {
        "username":"admin",
        "password":"admin123"
    }  
    response = await client.post("/users/login", json=payload)
    print(response.status_code)
    print(response.json())
    return response.json()["access_token"]