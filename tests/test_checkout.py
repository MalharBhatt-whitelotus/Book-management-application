import pytest

from get_token import get_token

@pytest.mark.asyncio
async def test_checkout(client):
    token = await get_token(client)
    payload = {"items":[{"book_id": 1, "quantity": 1}]}
    response = await client.post("/bills/checkout",json=payload, headers={"Authorization": f"bearer {token}"})
    assert response.status_code == 201
    result = response.json()
    assert result["total_amount"]> 0    