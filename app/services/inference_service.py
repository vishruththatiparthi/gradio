todos = []

def create_todo(task: str):
    todo = {
        "id": len(todos) + 1,
        "task": task
    }
    todos.append(todo)
    return todo


def get_todos():
    return todos


def update_todo(todo_id: int, task: str):
    for todo in todos:
        if todo["id"] == todo_id:
            todo["task"] = task
            return todo
    return {"error": "Todo not found"}


def delete_todo(todo_id: int):
    for todo in todos:
        if todo["id"] == todo_id:
            todos.remove(todo)
            return {"message": "Todo deleted"}
    return {"error": "Todo not found"}