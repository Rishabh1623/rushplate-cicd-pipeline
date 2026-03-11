from pydantic import BaseModel
from typing import List
from enum import Enum

class OrderStatus(str, Enum):
    placed = "placed"
    preparing = "preparing"
    picked_up = "picked_up"
    delivered = "delivered"

class OrderItem(BaseModel):
    menu_item_id: int
    quantity: int

class OrderCreate(BaseModel):
    restaurant_id: int
    items: List[OrderItem]
    delivery_address: str

class Order(BaseModel):
    id: int
    restaurant_id: int
    items: List[OrderItem]
    delivery_address: str
    status: OrderStatus
    total: float
