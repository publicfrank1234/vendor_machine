# Assuming you have an endpoint to create users and it works correctly
from app.routers.products import products


def test_deposit_and_buy_product(client):
    # Create user first
    user_response = client.post(
        "/users/",
        json={"username": "testbuyer", "password": "testpass", "role": "buyer"},
    )
    assert user_response.status_code == 200, "Failed to create user"
    user_id = user_response.json()["id"]
    print("created user:", user_id)

    # Deposit money for the user
    deposit_response = client.post(f"/deposit/", json={"amount": 100})
    print("deposit response: ", deposit_response.json())
    assert deposit_response.status_code == 200, "Failed to deposit"

    # Assuming you have a product setup in your fixture or beforehand in the test
    product_id = 1  # This should match an existing product
    buy_response = client.post(f"/buy/", json={"product_id": product_id, "quantity": 1})
    print(f"buy response: {buy_response.json()} and products are {products}")
    assert buy_response.status_code == 200, "Failed to buy product"
    assert (
        buy_response.json()["remaining_balance"] == 100 - products[product_id]["price"]
    ), "Incorrect balance after purchase"


def test_reset_deposit(client):
    user_id = 1
    client.post(f"/deposit/", json={"amount": 100})
    response = client.post(f"/reset/")
    assert response.status_code == 200
    assert response.json()["message"] == "Balance reset successful"
