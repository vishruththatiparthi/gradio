import gradio as gr
import requests
import os

# ---------------------------------
# API BASE URL
# ---------------------------------
API_BASE = os.getenv("API_URL", "http://api:8000/api/v1")
TODOS_URL = f"{API_BASE}/todos"
AUTH_URL = f"{API_BASE}/auth"

# ---------------------------------
# AUTH FUNCTIONS
# ---------------------------------
def register_user(username, password):
    try:
        r = requests.post(f"{AUTH_URL}/register", json={"username": username, "password": password})
        if r.status_code == 200:
            return "Registration successful! Please login."
        return f"Error: {r.json().get('detail', 'Unknown error')}"
    except Exception as e:
        return f"Connection error: {e}"


def login_user(username, password):
    try:
        r = requests.post(f"{AUTH_URL}/login", data={"username": username, "password": password})
        if r.status_code == 200:
            token = r.json().get("access_token")
            return f"Login successful!", token, gr.update(visible=True), gr.update(visible=False)
        return f"Error: {r.json().get('detail', 'Incorrect credentials')}", "", gr.update(visible=False), gr.update(visible=True)
    except Exception as e:
        return f"Connection error: {e}", "", gr.update(visible=False), gr.update(visible=True)

def logout_user():
    return "Logged out", "", gr.update(visible=False), gr.update(visible=True)

# ---------------------------------
# TODO API HELPER
# ---------------------------------
def get_headers(token):
    return {"Authorization": f"Bearer {token}"} if token else {}

# ---------------------------------
# EXECUTING ACTIONS
# ---------------------------------
def load_todos(token):
    if not token: return []
    try:
        r = requests.get(TODOS_URL, headers=get_headers(token))
        if r.status_code == 200:
            return [[t["id"], t["task"]] for t in r.json()]
        return []
    except Exception as e:
        print("Error:", e)
        return []

def get_todo(todo_id, token):
    if not token: return []
    try:
        r = requests.get(f"{TODOS_URL}/{int(todo_id)}", headers=get_headers(token))
        if r.status_code == 200:
            data = r.json()
            return [[data["id"], data["task"]]]
        return []
    except:
        return []

def create_todo(task, token):
    if token:
        try:
            requests.post(TODOS_URL, json={"task": task}, headers=get_headers(token))
        except: pass
    return load_todos(token)

def update_todo(todo_id, task, token):
    if token:
        try:
            requests.put(f"{TODOS_URL}/{int(todo_id)}", json={"task": task}, headers=get_headers(token))
        except: pass
    return load_todos(token)

def delete_todo(todo_id, token):
    if token:
        try:
            requests.delete(f"{TODOS_URL}/{int(todo_id)}", headers=get_headers(token))
        except: pass
    return load_todos(token)


# ---------------------------------
# UI
# ---------------------------------
with gr.Blocks(title="Todo App") as demo:

    token_state = gr.State("")

    gr.Markdown("# 📝 Validated Todo Application")

    # Display these blocks based on Auth State
    with gr.Column(visible=True) as login_pane:
        gr.Markdown("## Login / Register")
        with gr.Tab("Login"):
            l_user = gr.Textbox(label="Username")
            l_pass = gr.Textbox(label="Password", type="password")
            l_btn = gr.Button("Login")
            l_res = gr.Markdown("")
        
        with gr.Tab("Register"):
            r_user = gr.Textbox(label="Username")
            r_pass = gr.Textbox(label="Password", type="password")
            r_btn = gr.Button("Register")
            r_res = gr.Markdown("")

    with gr.Column(visible=False) as app_pane:
        with gr.Row():
            welcome_msg = gr.Markdown("## You are Logged In")
            logout_btn = gr.Button("Logout", size="sm")

        with gr.Tabs():
            with gr.Tab("All Todos"):
                all_table = gr.Dataframe(headers=["ID", "Task"], interactive=False)
                load_btn = gr.Button("Load Todos")
                load_btn.click(load_todos, inputs=token_state, outputs=all_table)

            with gr.Tab("Get Todo by ID"):
                todo_id_input = gr.Number(label="Todo ID")
                get_btn = gr.Button("Fetch")
                single_table = gr.Dataframe(headers=["ID", "Task"], interactive=False)
                get_btn.click(get_todo, inputs=[todo_id_input, token_state], outputs=single_table)

            with gr.Tab("Manage Todos"):
                new_task = gr.Textbox(label="New Task")
                create_btn = gr.Button("Create")
                manage_table = gr.Dataframe(headers=["ID", "Task"], interactive=False)
                create_btn.click(create_todo, inputs=[new_task, token_state], outputs=manage_table)

                gr.Markdown("---")
                update_id = gr.Number(label="Todo ID")
                update_task = gr.Textbox(label="Updated Task")
                update_btn = gr.Button("Update")
                update_btn.click(update_todo, inputs=[update_id, update_task, token_state], outputs=manage_table)

                gr.Markdown("---")
                delete_id = gr.Number(label="Todo ID")
                delete_btn = gr.Button("Delete")
                delete_btn.click(delete_todo, inputs=[delete_id, token_state], outputs=manage_table)

    # Auth wireups
    r_btn.click(register_user, inputs=[r_user, r_pass], outputs=r_res)
    l_btn.click(login_user, inputs=[l_user, l_pass], outputs=[l_res, token_state, app_pane, login_pane])
    logout_btn.click(logout_user, outputs=[l_res, token_state, app_pane, login_pane])


# ---------------------------------
# LAUNCH
# ---------------------------------
demo.launch(server_name="0.0.0.0", server_port=7860, show_error=True)