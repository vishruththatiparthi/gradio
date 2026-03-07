import gradio as gr
import requests

BASE_URL = "http://127.0.0.1:8000/api/v1/todos"


# Fetch todos and format for table
def load_todos():
    r = requests.get(f"{BASE_URL}/")
    data = r.json()

    table = []
    for t in data:
        table.append([t["id"], t["task"]])

    return table


# Create
def create_todo(task):
    requests.post(f"{BASE_URL}/", params={"task": task})
    return load_todos()


# Update
def update_todo(todo_id, task):
    requests.put(f"{BASE_URL}/{int(todo_id)}", params={"task": task})
    return load_todos()


# Delete
def delete_todo(todo_id):
    requests.delete(f"{BASE_URL}/{int(todo_id)}")
    return load_todos()


with gr.Blocks() as demo:

    gr.Markdown("# Todo Manager")

    todo_table = gr.Dataframe(
        headers=["ID", "Task"],
        interactive=False
    )

    load_btn = gr.Button("Refresh Todos")
    load_btn.click(load_todos, outputs=todo_table)

    with gr.Row():

        with gr.Column():
            gr.Markdown("### reate Todo")
            new_task = gr.Textbox(label="Task")
            create_btn = gr.Button("Create")
            create_btn.click(create_todo, inputs=new_task, outputs=todo_table)

        with gr.Column():
            gr.Markdown("### Update Todo")
            update_id = gr.Number(label="Todo ID")
            update_task = gr.Textbox(label="New Task")
            update_btn = gr.Button("Update")
            update_btn.click(update_todo, inputs=[update_id, update_task], outputs=todo_table)

        with gr.Column():
            gr.Markdown("### Delete Todo")
            delete_id = gr.Number(label="Todo ID")
            delete_btn = gr.Button("Delete")
            delete_btn.click(delete_todo, inputs=delete_id, outputs=todo_table)

demo.launch()