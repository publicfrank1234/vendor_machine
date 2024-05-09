from typing import Dict

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.dependencies import buyer_role_required
from app.models import Product, User

from .products import products

router = APIRouter()
# Simulating a balance storage for each user
user_balances: Dict[int, int] = {}


class DepositInput(BaseModel):
    amount: int


class BuyInput(BaseModel):
    product_id: int
    quantity: int


@router.post("/deposit/")
def deposit(deposit_input: DepositInput, user: dict = Depends(buyer_role_required)):
    amount = deposit_input.amount
    user_id = user.id
    print("user balances are : ", user_balances)
    if amount not in [5, 10, 20, 50, 100]:
        raise HTTPException(status_code=400, detail="Invalid coin amount")
    if user_id in user_balances:
        user_balances[user_id] += amount
    else:
        user_balances[user_id] = amount
    return {"message": "Deposit successful", "total_balance": user_balances[user_id]}


@router.post("/buy/")
def buy(buy_input: BuyInput, user: dict = Depends(buyer_role_required)):
    buyer_id = user.id
    product_id = int(buy_input.product_id)
    quantity = buy_input.quantity
    print("product request : ", product_id, quantity)
    print("user balances are : ", user_balances)
    print("products are : ", products)
    print("product details : ", products.get(product_id))
    if product_id not in products or products[product_id].get("quantity", 0) < quantity:
        raise HTTPException(
            status_code=404, detail="Product not available or insufficient quantity"
        )
    total_cost = products[product_id].get("price", 0) * quantity
    if buyer_id not in user_balances or user_balances[buyer_id] < total_cost:
        raise HTTPException(status_code=400, detail="Insufficient balance")
    products[product_id]["quantity"] = (
        products[product_id].get("quantity", 0) - quantity
    )
    user_balances[buyer_id] -= total_cost
    return {
        "message": "Purchase successful",
        "product": products[product_id].get("name"),
        "quantity": quantity,
        "spent": total_cost,
        "remaining_balance": user_balances[buyer_id],
    }


@router.post("/reset/")
def reset(user: dict = Depends(buyer_role_required)):
    user_id = user.id
    user_balances[user_id] = 0
    return {"message": "Balance reset successful"}
