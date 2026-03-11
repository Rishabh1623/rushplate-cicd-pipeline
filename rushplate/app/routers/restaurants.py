from fastapi import APIRouter, HTTPException
from app.models.restaurant import Restaurant, MenuItem

router = APIRouter()

# Mock data (simulates DB)
RESTAURANTS = [
    Restaurant(
        id=1, name="Pizza Hub", cuisine="Italian", rating=4.5,
        delivery_time="25-35 min",
        menu=[
            MenuItem(id=1, name="Margherita Pizza", price=12.99, description="Classic tomato & mozzarella"),
            MenuItem(id=2, name="Pepperoni Pizza", price=14.99, description="Loaded with pepperoni"),
            MenuItem(id=3, name="Garlic Bread", price=4.99, description="Toasted with garlic butter"),
        ]
    ),
    Restaurant(
        id=2, name="Burger Barn", cuisine="American", rating=4.2,
        delivery_time="20-30 min",
        menu=[
            MenuItem(id=4, name="Classic Burger", price=9.99, description="Beef patty with lettuce & tomato"),
            MenuItem(id=5, name="Cheese Burger", price=11.99, description="Double cheese beef burger"),
            MenuItem(id=6, name="Fries", price=3.99, description="Crispy golden fries"),
        ]
    ),
    Restaurant(
        id=3, name="Sushi World", cuisine="Japanese", rating=4.8,
        delivery_time="35-45 min",
        menu=[
            MenuItem(id=7, name="Salmon Roll", price=13.99, description="Fresh salmon maki roll"),
            MenuItem(id=8, name="Dragon Roll", price=16.99, description="Prawn tempura & avocado"),
            MenuItem(id=9, name="Miso Soup", price=3.49, description="Traditional Japanese soup"),
        ]
    ),
]

@router.get("/restaurants", response_model=list[Restaurant])
def get_restaurants():
    return RESTAURANTS

@router.get("/restaurants/{restaurant_id}", response_model=Restaurant)
def get_restaurant(restaurant_id: int):
    restaurant = next((r for r in RESTAURANTS if r.id == restaurant_id), None)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return restaurant
