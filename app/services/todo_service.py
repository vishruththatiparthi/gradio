todos = []


def create_todo(task: str):
    todo = {"id": len(todos) + 1, "task": task}
    todos.append(todo)
    return todo


def get_todos():
    return todos


def get_todo(todo_id: int):
    for todo in todos:
        if todo["id"] == todo_id:
            return todo
    return None


def update_todo(todo_id: int, task: str):
    todo = get_todo(todo_id)
    if not todo:
        return None

    todo["task"] = task
    return todo


def delete_todo(todo_id: int):
    todo = get_todo(todo_id)
    if not todo:
        return False

    todos.remove(todo)
    return True
