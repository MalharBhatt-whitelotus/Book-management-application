import pytest

from get_token import get_token

@pytest.mark.asyncio
async def test_bills(client):
    token = await get_token(client)
    response = await client.get("/bills/",headers={"Authorization":f"bearer {token}"})
    assert response.status_code == 200