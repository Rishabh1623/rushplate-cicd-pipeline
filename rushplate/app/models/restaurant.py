from pydantic import BaseModel
from typing import List, Optional

class MenuItem(BaseModel):
    id: int
    name: str
    price: float
    description: str

class Restaurant(BaseModel):
    id: int
    name: str
    cuisine: str
    rating: float
    delivery_time: str
    menu: List[MenuItem]
