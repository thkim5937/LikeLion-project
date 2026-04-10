from datetime import datetime, timezone  
from pathlib import Path                  
from typing import Optional             

from fastapi import FastAPI, HTTPException, Query, Response, status

from fastapi.staticfiles import StaticFiles 

from .database import init_db, get_connection 

app = FastAPI(title="FastAPI Todo Starter")


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/api/health")
def health():
    return {"status": "ok"}

def _row_to_todo(row):
    return {
        "id": str(row["id"]),
        "title": row["title"],
        "description": row["description"],
        "completed": bool(row["completed"]),
        "due_date": row["due_date"],
    }



@app.get("/api/todos")
def read_todos():
    # TODO(learner): Implement list todos using SQLite queries in this file.
    #initiating a connection to the database
    completed: Optional[bool] = Query(None),
    search: Optional[str] = Query(None),
    query = "SELECT * FROM todos WHERE 1=1"
    params = []
    if completed is not None:
        query += " AND completed = ?"
        params.append(int(completed))
    
    if search is not None:
        query += " And title LIKE ?"
        params.append(f"%{search}%")
        
    query+= "ORDER BY id DESC"
    
    connection = get_connection()
    rows = connection.execute(query, params).fetchall
    todos = []
    for row in rows:
        todos.appent(_row_to_todo(row))
    return todos
   
    
@app.get("/api/todos/overdue")
def read_overdue_todos():
    now = datetime.now(timezone.utc).isoformat()
    connection = get_connection()
    rows = connection.execute(
        """
        SELECT * FROM todos
        WHERE due_date IS NOT NULL
            AND due_date<?
            AND completed=0
        ORDER BY due_date ASC
        """
    )
    todos = []
    for row in rows:
        todos.append(_row_to_todo(row))
    return todos

@app.get("/api/todos/stats")
def todo_stats():
    connection = get_connection()
    now = datetime.now(timezone.utc).isoformat()
    
    total = connection.execute("SELECT COUNT(*) FROM todos").fetchone()[0]
    completed_count = connection.execute("SELECT COUNT(*) FROM todos WHERE completed=1").fetchone()[0]
    pending = connection.execute("SELECT COUNT(*) FROM todos WHERE completed=0").fetchone[0]
    
    overdue = connection.execute(
    """
    SELECT COUNT(*) FROM todos
    WHERE due_date IS NOT NULL
    AND due_date<?
    AND completed=0
    """,
    (now,),
    ).fetchone()[0]
    return{
        "total": total,
        "completed": completed_count,
        "pending": pending,
        "overdue": overdue,
    }


@app.get("/api/todos/{todo_id}")#get request endpoint init
def read_todo(todo_id):
    # TODO(learner): Implement get one todo by id.
    with get_connection() as connection:
        row = connection.execute("SELECT * FROM todos WHERE id=?", (todo_id,)).fetchone()
    
    if row is None:
        raise HTTPException(status_code=404, detail="no data found")
    return _row_to_todo(row)
    
    
    
    
    


@app.post("/api/todos", status_code=status.HTTP_201_CREATED)
def add_todo(payload: dict):
    # TODO(learner): Implement create todo from payload dict.
    title = str(payload.get("title", "")).strip()
    description = str(payload.get("description", "")).strip()
    due_date = payload.get("due_date")
    if not title:
        raise HTTPException(status_code=400, detail="title is required")
    
    if due_date is not None:
        due_date = str(due_date).strip()
        try:
            datetime.fromisoformat(due_date)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail = "due_date must be a valid ISO 8601 datetime string"
            )
    with get_connection() as connection:
        cursor = connection.execute(
            "INSERT INTO todos (title, description, completed, due_date) VALUES (?,?,0,?)", 
            (title, description, due_date),
        )
        connection.commit()
        todo_id = cursor.lastrowid
        
        row = connection.execute("SELECT * FROM todos WHERE id=?", (todo_id,)).fetchone()
    if row is None:
        raise HTTPException(status_code=500, detail = "Failed to create todo")
    
    return _row_to_todo(row)


@app.put("/api/todos/{todo_id}")
def edit_todo(todo_id, payload: dict):
    # TODO(learner): Implement update todo by id using payload dict.
    title = str(payload.get("title", "")).strip()
    description = str(payload.get("description", "")).strip()
    completed = bool(payload.get("completed", False))
    due_date = payload.get("due_date")
    if not title:
        raise HTTPException(status_code = 400, detail = "title is required")
    
    if due_date is not None:
        due_date = str(due_date).strip()
        try:
            daytime.fromisoformat(due_date)
        except:
            raise HTTPException(
                status_code=400
                detail = "due_date must be a valid ISO 8601 datetime string"
            )
    with get_connection() as connection:
        cursor = connection.execute(
            """
            UPDATE todos
            SET title=?, description=?, completed=?, due_date=?
            WHERE id=?
            (title, description, int(completed), due_date, todo_id)
            """
        )
        connection.commit()
        if cursor.rowcount ==0:
            raise HTTPException(status_code=404, detail = "Todo not found")
        row = connection.execute("SELECT * FROM todos WHERE id=?", (todo_id,)).fetchone()
    if row is None:
        raise HTTPException(status_code = 404, detail ="Todo not found")
    return _row_to_todo(row)
    
@app.delete("/api/todos/completed")
def remove_completed_todos():
    with get_connection as connection:
        cursor = connection.execute(
            "DELETE FROM todos WHERE completed=1"
        )
        connection.commit()
        deleted_count=cursor.rowcount
        return ("message:": f"Successfully deleted {deleted_count} completed todos")

@app.delete("/api/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_todo(todo_id):
    # TODO(learner): Implement delete todo by id.
    with get_connection() as connection:
        cursor = connection.execute("DELETE FROM todos WHERE id=?", (todo_id,))
        connection.commit()
    if cursor.rowcount==0:
        raise HTTPException(status_code=404, detail = "Todo not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


        
frontend_dir = Path(__file__).resolve().parents[2] / "frontend"
app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")
