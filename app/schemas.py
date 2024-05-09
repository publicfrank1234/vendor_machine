from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    password: str
    role: str


class UserDisplay(BaseModel):
    id: int
    username: str
    role: str


class UserUpdate(BaseModel):
    username: str
    password: str
    role: str


class ProductCreate(BaseModel):
    name: str
    price: int
    quantity: int


class ProductDisplay(BaseModel):
    id: int
    name: str
    price: int
    quantity: int
    quantity: int
