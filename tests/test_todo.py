import pytest

@pytest.fixture(scope="module")
def auth_token(client):
    client.post(
        "/api/v1/auth/register",
        json={"username": "todouser", "password": "password123"},
    )
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "todouser", "password": "password123"},
    )
    return response.json()["access_token"]


@pytest.fixture(scope="module")
def auth_headers(auth_token):
    return {"Authorization": f"Bearer {auth_token}"}


def test_create_todo(client, auth_headers):
    response = client.post(
        "/api/v1/todos/todos",
        json={"task": "Write Tests"},
        headers=auth_headers
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["task"] == "Write Tests"
    assert "id" in data


def test_get_todos(client, auth_headers):
    response = client.get("/api/v1/todos/todos", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["task"] == "Write Tests"


def test_update_todo(client, auth_headers):
    todos = client.get("/api/v1/todos/todos", headers=auth_headers).json()
    todo_id = todos[0]["id"]
    
    response = client.put(
        f"/api/v1/todos/todos/{todo_id}",
        json={"task": "Updated Task"},
        headers=auth_headers
    )
    assert response.status_code == 200
    assert response.json()["task"] == "Updated Task"


def test_delete_todo(client, auth_headers):
    todos = client.get("/api/v1/todos/todos", headers=auth_headers).json()
    todo_id = todos[0]["id"]

    response = client.delete(f"/api/v1/todos/todos/{todo_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Todo deleted"

    # Verify deletion
    response = client.get(f"/api/v1/todos/todos/{todo_id}", headers=auth_headers)
    assert response.status_code == 404
