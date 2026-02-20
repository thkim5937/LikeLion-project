const API_BASE = "/api/todos";

const todoForm = document.getElementById("todo-form");
const todoList = document.getElementById("todo-list");
const refreshBtn = document.getElementById("refresh-btn");

async function fetchTodos() {
  const response = await fetch(API_BASE);
  const todos = await response.json();
  renderTodos(todos);
}

function renderTodos(todos) {
  todoList.innerHTML = "";

  if (!todos.length) {
    const empty = document.createElement("li");
    empty.className = "empty";
    empty.textContent = "No todos yet.";
    todoList.appendChild(empty);
    return;
  }

  todos.forEach((todo) => {
    const li = document.createElement("li");
    li.className = todo.completed ? "todo completed" : "todo";

    li.innerHTML = `
      <div class="todo-body">
        <h3>${escapeHtml(todo.title)}</h3>
        <p>${escapeHtml(todo.description || "No description")}</p>
      </div>
      <div class="actions">
        <button data-action="toggle">${todo.completed ? "Undo" : "Done"}</button>
        <button data-action="delete" class="danger">Delete</button>
      </div>
    `;

    li.querySelector('[data-action="toggle"]').addEventListener("click", async () => {
      await updateTodo(todo.id, {
        title: todo.title,
        description: todo.description,
        completed: !todo.completed,
      });
      fetchTodos();
    });

    li.querySelector('[data-action="delete"]').addEventListener("click", async () => {
      await deleteTodo(todo.id);
      fetchTodos();
    });

    todoList.appendChild(li);
  });
}

async function createTodo(payload) {
  await fetch(API_BASE, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
}

async function updateTodo(id, payload) {
  await fetch(`${API_BASE}/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
}

async function deleteTodo(id) {
  await fetch(`${API_BASE}/${id}`, { method: "DELETE" });
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

todoForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  const formData = new FormData(todoForm);
  const title = (formData.get("title") || "").toString().trim();
  const description = (formData.get("description") || "").toString().trim();

  if (!title) {
    return;
  }

  await createTodo({ title, description });
  todoForm.reset();
  fetchTodos();
});

refreshBtn.addEventListener("click", fetchTodos);

fetchTodos();
