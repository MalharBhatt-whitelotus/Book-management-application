import pytest
from get_token import get_token
@pytest.mark.asyncio
async def test_get_books(client):
    token = await get_token(client)
    response = await client.get("/books/", headers= {"Authorization":f"bearer {token}"})
    print(response.status_code)
    print(response.headers)
    print(response.text)
    assert response.status_code == 200
    books = response.json()
    assert isinstance(books,list)