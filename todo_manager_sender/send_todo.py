from fastapi import FastAPI, HTTPException
import requests
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

url = 'http://localhost:8000/webhook/todo-added'

class Todo(BaseModel):
    id: int
    title: str
    description: Optional[str] = None

def get_todo_input():
    title = input("Enter todo title: ")
    description = input("Enter description (press Enter to skip): ").strip()
    return title, description if description else None

def send_todo_to_webhook(todo: Todo):
    try:
        response = requests.post(url, json=todo.dict())
        response.raise_for_status()
        print(f"Successfully sent todo: {todo.title}")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error sending todo: {str(e)}")
        return None

@app.get('/')
async def root():
    todo_id = 1
    while True:
        title, description = get_todo_input()
        todo = Todo(id=todo_id, title=title, description=description)
        result = send_todo_to_webhook(todo)

        if result:
            print("Todo sent successfully!")
        else:
            print("Failed to send todo. Please try again.")

        continue_input = input("Do you want to add another todo? (y/n): ").lower()
        if continue_input != 'y':
            break
        todo_id += 1

    return {"message": "Todo input session ended"}