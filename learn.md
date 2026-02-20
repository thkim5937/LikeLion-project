# FastAPI Learning Guide: Todo CRUD Assignment

This assignment teaches core FastAPI backend skills by implementing a TODO API that connects to a ready-made JavaScript frontend.

## Goal

Build a working backend in `backend/app/main.py` so the frontend can:
- Create todos
- View all todos
- View one todo
- Update a todo
- Delete a todo

Database setup is already done for you in `backend/app/database.py`.

## Prerequisites

- Basic Python syntax
- Basic HTTP concepts (GET, POST, PUT, DELETE)

## Files you will use

- `backend/app/main.py` (your assignment file)
- `backend/app/database.py` (already complete)
- `frontend/` (already complete UI)

Optional reference (check after trying yourself):
- `backend/app/main_solution.py`

## FastAPI Basics (Quick)

- `@app.get(...)`, `@app.post(...)`, `@app.put(...)`, `@app.delete(...)`: define route handlers.
- `HTTPException`: return API errors like 404.
- `status.HTTP_201_CREATED` / `status.HTTP_204_NO_CONTENT`: set status codes.
- Request bodies can be plain `dict` for this assignment.

## Assignment Steps

1. Start the app in student mode.

```bash
uvicorn backend.app.main:app --reload
```

2. Confirm server is running.
- Open `http://127.0.0.1:8000/api/health`
- Expected response: `{ "status": "ok" }`

3. Implement `read_todos` in `main.py`.
- Query all rows from `todos` table.
- Convert rows into plain dict objects with keys:
  - `id`
  - `title`
  - `description`
  - `completed`
- Return a list.

4. Implement `read_todo` in `main.py`.
- Query one row by `todo_id`.
- If row does not exist, raise `HTTPException(status_code=404, detail="Todo not found")`.
- Return a plain dict object.

5. Implement `add_todo` in `main.py`.
- Read data from a dict payload (`payload["title"]`, `payload.get("description", "")`).
- Insert row using title and description.
- Commit transaction.
- Fetch inserted row and return it as a plain dict.

6. Implement `edit_todo` in `main.py`.
- Read `title`, `description`, and `completed` from dict payload.
- Update row by `todo_id`.
- If nothing updated, return 404.
- Fetch updated row and return it as a plain dict.

7. Implement `remove_todo` in `main.py`.
- Delete row by `todo_id`.
- If nothing deleted, return 404.
- Return `204 No Content`.

8. Test from the API docs.
- Open `http://127.0.0.1:8000/docs`
- Run each endpoint and verify status codes.

9. Test from frontend.
- Open `http://127.0.0.1:8000/`
- Try add/update/delete from UI.

## Expected Behaviors

- GET all returns a list, possibly empty.
- GET by id returns item or 404.
- POST returns 201 with created todo.
- PUT returns updated todo or 404.
- DELETE returns 204 or 404.

## Common Mistakes

- Forgetting `connection.commit()` on write operations.
- Returning raw sqlite rows instead of plain dicts.
- Not converting `completed` to `bool` in responses.
- Missing 404 handling for not-found IDs.

## Stretch Tasks

- Add a due date field.
- Add filtering (`completed=true/false`).
- Add pagination (`limit`, `offset`).
- Add simple tests with `pytest` + `TestClient`.

## Submission Suggestion

- Submit your `backend/app/main.py`.
- Include short notes:
  - What worked
  - What was hard
  - What you would improve next
