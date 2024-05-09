from typing import Dict

from pydantic import BaseModel


class User(BaseModel):
    id: int
    username: str
    hashed_password: str
    role: str  # "buyer" or "seller"


class Product(BaseModel):
    id: int
    name: str
    price: int  # Price in cents
    quantity: int
    seller_id: int  # ID of the user who is the seller
