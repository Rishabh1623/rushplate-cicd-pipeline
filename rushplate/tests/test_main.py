from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_get_restaurants():
    response = client.get("/restaurants")
    assert response.status_code == 200
    assert len(response.json()) == 3

def test_get_restaurant_by_id():
    response = client.get("/restaurants/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Pizza Hub"

def test_get_restaurant_not_found():
    response = client.get("/restaurants/999")
    assert response.status_code == 404

def test_place_order():
    response = client.post("/orders", json={
        "restaurant_id": 1,
        "items": [{"menu_item_id": 1, "quantity": 2}],
        "delivery_address": "123 Test Street"
    })
    assert response.status_code == 200
    assert response.json()["status"] == "placed"
    assert response.json()["total"] == 25.98

def test_get_orders():
    response = client.get("/orders")
    assert response.status_code == 200

def test_get_order_not_found():
    response = client.get("/orders/999")
    assert response.status_code == 404
