
from app.services.ai import search_products, calculate_total


def test_search_keyboard():
    results = search_products(query="keyboard")

    assert len(results) == 1
    assert results[0]["name"] == "Keyboard"


def test_search_mouse():
    results = search_products(query="mouse")

    assert len(results) == 1
    assert results[0]["name"] == "Wireless Gaming Mouse"


def test_search_price_filter():
    results = search_products(max_price=40)

    names = [product["name"] for product in results]

    assert "Wireless Gaming Mouse" in names
    assert "Keyboard" not in names
    assert "Monitor" not in names


def test_search_no_matches():
    results = search_products(query="laptop")

    assert results == []


def test_calculate_total():
    result = calculate_total(product_id=2, quantity=2)

    assert result["status"] == "success"
    assert result["unit_price"] == 35.0
    assert result["total"] == 70.0

def test_calculate_total_product_not_found():
    result = calculate_total(product_id=999, quantity=2)

    assert result["status"] == "not_found"
    assert "total" not in result