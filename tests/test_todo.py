import pytest

pytestmark = pytest.mark.anyio

from app.api.v1.endpoints import todo as todo_endpoint
from app.services import todo_service


@pytest.fixture
def reset_todos():
    todo_service.todos.clear()


@pytest.fixture
async def sample_todo(reset_todos):
    return await todo_endpoint.create(task="Learn FastAPI")


async def test_create_todo(reset_todos):
    response = await todo_endpoint.create(task="Write Tests")
    assert response["id"] == 1
    assert response["task"] == "Write Tests"


async def test_get_todos(sample_todo):
    response = await todo_endpoint.read()
    assert len(response) == 1
    assert response[0]["task"] == "Learn FastAPI"


async def test_update_todo(sample_todo):
    todo_id = sample_todo["id"]
    response = await todo_endpoint.update(todo_id=todo_id, task="Updated Task")
    assert response["id"] == todo_id
    assert response["task"] == "Updated Task"


async def test_delete_todo(sample_todo):
    todo_id = sample_todo["id"]
    response = await todo_endpoint.delete(todo_id=todo_id)
    assert response["message"] == "Todo deleted"
