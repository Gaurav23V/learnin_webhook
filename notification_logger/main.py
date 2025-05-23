from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import sqlite3
from datetime import datetime

app = FastAPI()

# Database setup
def init_db():
    conn = sqlite3.connect('todos.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Initialize database on startup
init_db()

class Todo(BaseModel):
    id: int
    title: str
    description: Optional[str] = None

class TodoResponse(Todo):
    created_at: datetime

@app.get('/')
def root():
    return {"message": "Hello World"}

@app.post('/webhook/todo-added')
def todo_added(todo: Todo):
    try:
        # Log to database
        conn = sqlite3.connect('todos.db')
        c = conn.cursor()
        c.execute(
            'INSERT INTO todos (id, title, description) VALUES (?, ?, ?)',
            (todo.id, todo.title, todo.description)
        )
        conn.commit()
        conn.close()

        print(f"Todo added: {todo}")
        return {
            "status": "success",
            "message": "Todo received and logged successfully",
            "todo": todo.dict()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/todos', response_model=List[TodoResponse])
def get_all_todos():
    try:
        conn = sqlite3.connect('todos.db')
        c = conn.cursor()
        c.execute('SELECT id, title, description, created_at FROM todos ORDER BY created_at DESC')
        todos = c.fetchall()
        conn.close()

        return [
            TodoResponse(
                id=row[0],
                title=row[1],
                description=row[2],
                created_at=datetime.fromisoformat(row[3])
            )
            for row in todos
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))