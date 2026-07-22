const API_BASE = "/api/todos";

const todoForm = document.getElementById("todo-form");
const todoList = document.getElementById("todo-list");
const refreshBtn = document.getElementById("refresh-btn");
const statTotal = document.getElementById("stat-total");
const statCompleted = document.getElementById("stat-completed");
const statPending = document.getElementById("stat-pending");
const statOverdue = document.getElementById("stat-overdue");
const filterCompletedSelect = document.getElementById("filter-completed");
const filterSearchInput = document.getElementById("filter-search");
const deleteCompletedBtn = document.getElementById("delete-completed-btn");

async function fetchOverdueIds() {
  const response = await fetch(`${API_BASE}/overdue`);
  const overdueTodos = await response.json();
  return new Set(overdueTodos.map((todo) => todo.id));
}

async function fetchStats() {
  const response = await fetch(`${API_BASE}/stats`);
  const stats = await response.json();
  renderStats(stats);
}

function renderStats(stats) {
  statTotal.textContent = stats.total;
  statCompleted.textContent = stats.completed;
  statPending.textContent = stats.pending;
  statOverdue.textContent = stats.overdue;
}

async function fetchTodos() {
  const params = new URLSearchParams();
  const completed = filterCompletedSelect.value;
  const search = filterSearchInput.value.trim();
  if (completed) {
    params.set("completed", completed);
  }
  if (search) {
    params.set("search", search);
  }
  const query = params.toString();
  const url = query ? `${API_BASE}?${query}` : API_BASE;

  const [response, overdueIds] = await Promise.all([fetch(url), fetchOverdueIds()]);
  const todos = await response.json();
  renderTodos(todos, overdueIds);
  fetchStats();
}

function renderTodos(todos, overdueIds = new Set()) {
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
    if (overdueIds.has(todo.id)) {
      li.className += " overdue";
    }

    li.innerHTML = `
      <div class="todo-body">
        <h3>${escapeHtml(todo.title)}</h3>
        <p>${escapeHtml(todo.description || "No description")}</p>
        <p class="due-date">${todo.due_date ? "Due: " + escapeHtml(formatDueDate(todo.due_date)) : "No due date"}</p>
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
        due_date: todo.due_date,
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

async function deleteCompletedTodos() {
  await fetch(`${API_BASE}/completed`, { method: "DELETE" });
}

function debounce(fn, delay) {
  let timeoutId;
  return (...args) => {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => fn(...args), delay);
  };
}

function formatDueDate(isoString) {
  return new Date(isoString).toLocaleString("en-US", {
    year: "numeric",
    month: "long",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
    hour12: true,
  });
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

const formError = document.getElementById("form-error");
const dueDateTimeInput = document.getElementById("due-date-time-input");
const dueDateClearBtn = document.getElementById("due-date-clear");

const dueDatePicker = flatpickr(dueDateTimeInput, {
  enableTime: true,
  dateFormat: "Y-m-d\\TH:i:00",
  altInput: true,
  altFormat: "F j, Y h:i K",
  allowInput: false,
  clickOpens: true,
});

dueDateClearBtn.addEventListener("click", () => {
  dueDatePicker.clear();
});

function showFormError(message) {
  formError.textContent = message;
}

function clearFormError() {
  formError.textContent = "";
}

todoForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  const formData = new FormData(todoForm);
  const title = (formData.get("title") || "").toString().trim();
  const description = (formData.get("description") || "").toString().trim();
  const dueDateTimeDisplay = dueDatePicker.altInput.value.trim();

  if (!title) {
    showFormError("Title is required.");
    return;
  }

  let due_date = null;

  if (dueDateTimeDisplay) {
    due_date = dueDateTimeInput.value.trim();
  }

  clearFormError();

  await createTodo({ title, description, due_date });
  todoForm.reset();
  dueDatePicker.clear();
  fetchTodos();
});

refreshBtn.addEventListener("click", fetchTodos);

filterCompletedSelect.addEventListener("change", fetchTodos);

const debouncedFetchTodos = debounce(fetchTodos, 300);
filterSearchInput.addEventListener("input", debouncedFetchTodos);

deleteCompletedBtn.addEventListener("click", async () => {
  await deleteCompletedTodos();
  fetchTodos();
});

fetchTodos();
