def test_create_and_get_product(client):
    # Test product creation
    create_response = client.post(
        "/products/", json={"name": "Soda", "price": 100, "quantity": 50}
    )
    assert create_response.status_code == 200, "Failed to create product"
    product_id = create_response.json()["id"]

    # Test fetching the product
    get_response = client.get(f"/products/{product_id}")
    assert get_response.status_code == 200, "Product not found"
    assert get_response.json()["name"] == "Soda", "Product details do not match"


def test_product_not_found(client):
    response = client.get("/products/999")
    assert response.status_code == 404, "Product should not be found"


def test_update_product(client):
    # First, create a product to update
    create_response = client.post(
        "/products/", json={"name": "Water", "price": 50, "quantity": 100}
    )
    assert create_response.status_code == 200, "Failed to create product"
    product_id = create_response.json()["id"]

    # Update the product
    update_response = client.put(
        f"/products/{product_id}",
        json={"name": "Sparkling Water", "price": 75, "quantity": 50},
    )
    assert update_response.status_code == 200, "Failed to update product"
    assert (
        update_response.json()["name"] == "Sparkling Water"
    ), "Product update details do not match"


def test_delete_product(client):
    # First, create a product to delete
    create_response = client.post(
        "/products/", json={"name": "Juice", "price": 30, "quantity": 80}
    )
    assert create_response.status_code == 200, "Failed to create product"
    product_id = create_response.json()["id"]

    # Delete the product
    client.delete(f"/products/{product_id}")

    # Verify the product is no longer available
    get_response = client.get(f"/products/{product_id}")
    assert get_response.status_code == 404, "Product should not be found after deletion"
