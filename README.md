# FastAPI Todo Starter (Assignment)

A small project for FastAPI learners to practice building a basic CRUD backend.

## What is included

- FastAPI backend skeleton with TODO CRUD route declarations (`backend/app/main.py`)
- Finished reference implementation (`backend/app/main_solution.py`)
- SQLite database file (`backend/todo.db`) auto-created on startup
- JavaScript frontend already implemented and connected to backend routes

Important: `backend/app/main.py` is intentionally incomplete (`pass` + TODO comments). Learners should implement CRUD queries directly in `main.py`.
This starter uses plain dict payloads/responses to keep the first assignment simple.

## Project structure

```text
fastapi/
  backend/
    app/
      main.py
      main_solution.py
      database.py
  frontend/
    index.html
    app.js
    style.css
  learn.md
  requirements.txt
```

## Setup

1. Create and activate virtual environment
2. Install dependencies

```bash
pip install -r requirements.txt
```

## Run (Student Version)

```bash
uvicorn backend.app.main:app --reload
```

## Run (Reference Solution)

```bash
uvicorn backend.app.main_solution:app --reload
```

## Open

- App: http://127.0.0.1:8000/
- API docs: http://127.0.0.1:8000/docs

## API routes

- `GET /api/todos`
- `GET /api/todos/{todo_id}`
- `POST /api/todos`
- `PUT /api/todos/{todo_id}`
- `DELETE /api/todos/{todo_id}`

## Learning path

- Complete CRUD in `backend/app/main.py`
- Verify behavior from frontend and `/docs`
- Compare your result with `backend/app/main_solution.py`
- Follow `/Users/soohyeuk/Documents/llus/fastapi/learn.md` for step-by-step guidance
