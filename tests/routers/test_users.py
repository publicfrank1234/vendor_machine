# tests/routers/test_users.py
def test_create_user(client):
    response = client.post(
        "/users/",
        json={"username": "testuser", "password": "testpass", "role": "buyer"},
    )
    assert response.status_code == 200, "Failed to create user"
    assert response.json()["username"] == "testuser", "Username does not match"


def test_get_user(client):
    # Assuming test_create_user has run and the user exists
    create_response = client.post(
        "/users/",
        json={"username": "testuser2", "password": "testpass2", "role": "buyer"},
    )
    user_id = create_response.json()["id"]
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200, "User not found"
    assert response.json()["username"] == "testuser2", "User details do not match"


def test_update_user(client):
    # Create a user to update
    create_response = client.post(
        "/users/",
        json={"username": "testuser3", "password": "testpass3", "role": "buyer"},
    )
    user_id = create_response.json()["id"]
    # Update the user
    update_response = client.put(
        f"/users/{user_id}",
        json={"username": "updateduser", "password": "updatedpass", "role": "buyer"},
    )
    assert update_response.status_code == 200, "Failed to update user"
    assert (
        update_response.json()["username"] == "updateduser"
    ), "User update details do not match"


def test_delete_user(client):
    # Create a user to delete
    create_response = client.post(
        "/users/",
        json={"username": "testuser4", "password": "testpass4", "role": "buyer"},
    )
    user_id = create_response.json()["id"]
    # Delete the user
    delete_response = client.delete(f"/users/{user_id}")
    print(delete_response.json())
    assert delete_response.status_code == 200, "Failed to delete user"
    # Verify the user is no longer available
    get_response = client.get(f"/users/{user_id}")
    assert get_response.status_code == 404, "User should not be found after deletion"


def test_user_not_found(client):
    response = client.get("/users/999")
    assert response.status_code == 404
    assert response.status_code == 404
