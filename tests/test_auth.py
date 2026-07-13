import pytest

@pytest.mark.asyncio
async def test_login(client):
    payload ={
        "username": "admin",
        "password": "admin123"
    }

    response = await client.post("/users/login", json=payload)
    assert response.status_code == 200
    body = response.json()  
    assert "access_token" in body   