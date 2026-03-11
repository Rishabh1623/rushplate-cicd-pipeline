from fastapi import APIRouter, HTTPException
from app.models.order import Order, OrderCreate, OrderStatus
from app.routers.restaurants import RESTAURANTS

router = APIRouter()

# In-memory order store (simulates DB)
orders_db = []
order_counter = 1

def calculate_total(restaurant_id: int, items) -> float:
    restaurant = next((r for r in RESTAURANTS if r.id == restaurant_id), None)
    if not restaurant:
        return 0.0
    total = 0.0
    for item in items:
        menu_item = next((m for m in restaurant.menu if m.id == item.menu_item_id), None)
        if menu_item:
            total += menu_item.price * item.quantity
    return round(total, 2)

@router.post("/orders", response_model=Order)
def place_order(order: OrderCreate):
    global order_counter
    restaurant = next((r for r in RESTAURANTS if r.id == order.restaurant_id), None)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    total = calculate_total(order.restaurant_id, order.items)
    new_order = Order(
        id=order_counter,
        restaurant_id=order.restaurant_id,
        items=order.items,
        delivery_address=order.delivery_address,
        status=OrderStatus.placed,
        total=total
    )
    orders_db.append(new_order)
    order_counter += 1
    return new_order

@router.get("/orders", response_model=list[Order])
def get_orders():
    return orders_db

@router.get("/orders/{order_id}", response_model=Order)
def get_order(order_id: int):
    order = next((o for o in orders_db if o.id == order_id), None)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.put("/orders/{order_id}/status", response_model=Order)
def update_order_status(order_id: int, status: OrderStatus):
    order = next((o for o in orders_db if o.id == order_id), None)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order.status = status
    return order
