import gradio as gr
import requests
import os

# ---------------------------------
# API BASE URL
# ---------------------------------
BASE_URL = os.getenv(
    "API_URL",
    "http://api:8000/api/v1/todos/todos"   # Docker service name
)


# ---------------------------------
# GET ALL TODOS
# ---------------------------------
def load_todos():
    try:
        r = requests.get(BASE_URL)
        r.raise_for_status()
        data = r.json()
        return [[t["id"], t["task"]] for t in data]
    except Exception as e:
        print("Error loading todos:", e)
        return []


# ---------------------------------
# GET TODO BY ID
# ---------------------------------
def get_todo(todo_id):
    try:
        r = requests.get(f"{BASE_URL}/{int(todo_id)}")
        r.raise_for_status()
        data = r.json()
        return [[data["id"], data["task"]]]
    except Exception as e:
        print("Error fetching todo:", e)
        return []


# ---------------------------------
# CREATE TODO
# ---------------------------------
def create_todo(task):
    try:
        requests.post(BASE_URL, json={"task": task})
    except Exception as e:
        print("Create error:", e)
    return load_todos()


# ---------------------------------
# UPDATE TODO
# ---------------------------------
def update_todo(todo_id, task):
    try:
        requests.put(f"{BASE_URL}/{int(todo_id)}", json={"task": task})
    except Exception as e:
        print("Update error:", e)
    return load_todos()


# ---------------------------------
# DELETE TODO
# ---------------------------------
def delete_todo(todo_id):
    try:
        requests.delete(f"{BASE_URL}/{int(todo_id)}")
    except Exception as e:
        print("Delete error:", e)
    return load_todos()


# ---------------------------------
# UI
# ---------------------------------
with gr.Blocks(title="Todo App") as demo:

    gr.Markdown("# 📝 Todo Application")

    with gr.Tabs():

        # -------------------------
        # ALL TODOS
        # -------------------------
        with gr.Tab("All Todos"):

            gr.Markdown("## View All Todos")

            all_table = gr.Dataframe(
                headers=["ID", "Task"],
                interactive=False
            )

            load_btn = gr.Button("Load Todos")

            load_btn.click(
                load_todos,
                outputs=all_table
            )


        # -------------------------
        # GET BY ID
        # -------------------------
        with gr.Tab("Get Todo by ID"):

            gr.Markdown("## Fetch Specific Todo")

            todo_id_input = gr.Number(label="Todo ID")
            get_btn = gr.Button("Fetch")

            single_table = gr.Dataframe(
                headers=["ID", "Task"],
                interactive=False
            )

            get_btn.click(
                get_todo,
                inputs=todo_id_input,
                outputs=single_table
            )


        # -------------------------
        # MANAGE TODOS
        # -------------------------
        with gr.Tab("Manage Todos"):

            gr.Markdown("## Create Todo")

            new_task = gr.Textbox(label="Task")
            create_btn = gr.Button("Create")

            manage_table = gr.Dataframe(
                headers=["ID", "Task"],
                interactive=False
            )

            create_btn.click(
                create_todo,
                inputs=new_task,
                outputs=manage_table
            )


            gr.Markdown("## Update Todo")

            update_id = gr.Number(label="Todo ID")
            update_task = gr.Textbox(label="New Task")

            update_btn = gr.Button("Update")

            update_btn.click(
                update_todo,
                inputs=[update_id, update_task],
                outputs=manage_table
            )


            gr.Markdown("## Delete Todo")

            delete_id = gr.Number(label="Todo ID")
            delete_btn = gr.Button("Delete")

            delete_btn.click(
                delete_todo,
                inputs=delete_id,
                outputs=manage_table
            )


# ---------------------------------
# LAUNCH (Docker compatible)
# ---------------------------------
demo.launch(
    server_name="0.0.0.0",
    server_port=7860,
    show_error=True
)