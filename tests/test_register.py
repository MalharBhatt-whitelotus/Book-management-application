import pytest
import random

@pytest.mark.ayncion
async def tetst_regiter(client):
    number = random.randint(1,100000)
    payload = {
        "name": "test User",
        "email": f"User{number}@gmail.com",
        "password": "password123"}
    
    response = await client.post("/user/register", json=payload)
    assert response.status_code == 201