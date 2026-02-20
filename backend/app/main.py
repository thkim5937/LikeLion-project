from pathlib import Path

from fastapi import FastAPI, HTTPException, Response, status
from fastapi.staticfiles import StaticFiles

from .database import get_connection, init_db

app = FastAPI(title="FastAPI Todo Starter")


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/api/health")
def health():
    return {"status": "ok"}

def _row_to_todo(row):
    return {
        "id": row["id"],
        "title": row["title"],
        "description": row["description"],
        "completed": bool(row["completed"]),
    }

@app.get("/api/todos")
def read_todos():
    # TODO(learner): Implement list todos using SQLite queries in this file.
    #initiating a connection to the database
    connection = get_connection()
    
    #fetching all data from todos table
    data = connection.execute("SELECT * FROM todos").fetchall()
    
    todos =[]
    for row in data:
        
        todos.append({
            "id": row["id"],
            "title":row["title"],
            "description":row["description"],
            "completed":bool(row["completed"])
        })
    return todos


@app.get("/api/todos/{todo_id}")#get request endpoint init
def read_todo(todo_id):
    # TODO(learner): Implement get one todo by id.
    connection = get_connection()
    data = connection.execute("SELECT * FROM todos WHERE id=?", (todo_id,)).fetchone()
    
    if data is None:
        raise Exception("no data found")
    
    map= {"id": data["id"],
    "title":data["title"],
    "description":data["description"],
    "completed": bool(data["completed"])}
    return map
    


@app.post("/api/todos", status_code=status.HTTP_201_CREATED)
def add_todo(payload: dict):
    # TODO(learner): Implement create todo from payload dict.
    title = str(payload.get("title", "")).srtip()
    description = str(payload.get("description", "")).srtip()
    if not title:
        raise HTTPException(status_code=400, detail="title is required")
    
    with get_connection() as connection:
        cursor = connection.execute(
            "INSERT INTO todos (title, description, completed) VALUES (?,?,0)", 
            (title, description),
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
    title = str(payload.get("title", "")).srtip()
    description = str(payload.get("description", "")).srtip()
    completed = bool(payload.get("completed", False))
    
    if not title:
        raise HTTPException(status_code = 400, detail = "title is required")
    with get_connection() as connection:
        cursor = connection.execute(
            """
            UPDATE todos
            SET title=?, description=?, completed=?
            WHERE id=?
            (title, description, int(completed), todo_id)
            """
        )
        connection.commit()
        if cursor.rowcount ==0:
            raise HTTPException(status_code=404, detail = "Todo not found")
        row = connection.execute("SELECT * FROM todos WHERE id=?", (todo_id,)).fetchone()
    if row is None:
        raise HTTPException(status_code = 404, detail ="Todo not found")
    return _row_to_todo(row)
    


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
