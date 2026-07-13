import pytest

from get_token import get_token

@pytest.mark.asyncio
async def test_filter_category(client):
    token = await get_token(client)

    response = await client.get("/books/filter?category=Programming/", headers={"Authorization":f"Bearer {token}"})
    print(response.status_code)
    print(response.json())
    assert response.status_code == 200
    books = response.json()
    for book in books:
        assert "Programming" in book["category"]

@pytest.mark.asyncio
async def test_filter_available_books(client):
    token = await get_token(client)
    response = await client.get("/books/filter?available=true",headers={"Authorization":f"Bearer {token}"})
    assert response.status_code == 200
    books = response.json()
    for book in books:
        assert book["quantity"] > 0

@pytest.mark.asyncio
async def test_sort_price(client):
    token = await get_token(client)
    response = await client.get("/books/filter?sort_by=price&order=asc",headers={"Authorization":f"bearer {token}"})
    assert response.status_code == 200
    books = response.json()
    prices = [book["price"] for book in books]
    assert prices == sorted(prices)

@pytest.mark.asyncio
async def test_advance_filter(client):
    token = await get_token(client)
    response = await client.get("/books/filter?category=Programming&author=Robert C. Martin&book_type=hardcopy&min_price=300&max_price=1000&sort_by=price&order=desc",headers={"Authorization":f"Bearer {token}"})
    assert response.status_code == 200
    books  = response.json()
    prices = [book["price"] for book in books]
    assert prices == sorted(prices, reverse=True)
    for book in books:
        assert book["price"] >= 300
        assert book["price"] <= 1000
        assert book["category"] == "Programming"
        assert book["author"] == "Robert C. Martin"
        assert book["book_type"] == "hardcopy"
