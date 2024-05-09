from typing import Dict, List

from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies import seller_role_required
from app.models import Product
from app.schemas import ProductCreate, ProductDisplay

router = APIRouter()
products: Dict[int, Product] = {}
product_id_counter: int = 1


@router.post("/products/", response_model=ProductDisplay)
def create_product(
    product: ProductCreate, seller_id: int = Depends(seller_role_required)
):
    print("seller_id:", seller_id)
    global product_id_counter
    print(product, seller_id)
    new_product = Product(
        id=product_id_counter,
        name=product.name,
        price=product.price,
        quantity=product.quantity,
        seller_id=seller_id,
    )
    products[product_id_counter] = new_product
    product_id_counter += 1
    return new_product


@router.get("/products/", response_model=List[ProductDisplay])
def get_all_products():
    return list(products.values())


@router.get("/products/{product_id}", response_model=ProductDisplay)
def get_product(product_id: int):
    if product_id in products:
        return products[product_id]
    raise HTTPException(status_code=404, detail="Product not found")


@router.put("/products/{product_id}", response_model=ProductDisplay)
def update_product(
    product_id: int,
    product_data: ProductCreate,
    seller_id: int = Depends(seller_role_required),
):
    if product_id not in products:
        raise HTTPException(status_code=404, detail="Product not found")
    if products[product_id].seller_id != seller_id:
        raise HTTPException(
            status_code=403, detail="Not authorized to update this product"
        )
    product = products[product_id]
    product.name = product_data.name
    product.price = product_data.price
    product.quantity = product_data.quantity
    products[product_id] = product  # Update the product
    return product


@router.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, seller_id: int = Depends(seller_role_required)):
    if product_id not in products:
        raise HTTPException(status_code=404, detail="Product not found")
    if products[product_id].seller_id != seller_id:
        raise HTTPException(
            status_code=403, detail="Not authorized to delete this product"
        )
    del products[product_id]
    return {"detail": "Product deleted successfully"}
