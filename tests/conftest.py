import pytest
from fastapi.testclient import TestClient

from app.dependencies import get_current_user, seller_role_required
from app.main import app  # Ensure your FastAPI main application is imported correctly
from app.routers.products import products  # Import the actual products dictionary


@pytest.fixture(autouse=True)
def reset_app_state():
    from app.routers.products import products

    products.clear()  # Assuming `products` is a dictionary storing product data
    products.update(
        {
            1: {"id": 1, "name": "Cola", "price": 20, "quantity": 50},
            2: {"id": 2, "name": "Water", "price": 100, "quantity": 30},
        }
    )


@pytest.fixture
def client():
    # Apple this to seller_role_required directly
    def override_seller_role_required():
        # return {"id": 1, "username": "authorized_user", "role": "buyer"}  # Mock user
        return 1

    # Apply this to buyer_role
    def override_get_current_user():
        # return {"id": 1, "username": "authorized_user", "role": "seller"}  # Mock user
        return 1

    # Apply the override globally for all tests
    app.dependency_overrides[seller_role_required] = override_seller_role_required
    app.dependency_overrides[get_current_user] = override_get_current_user

    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()  # Clear overrides after tests
