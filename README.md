# Todo Webhook System

This project demonstrates a simple webhook-based todo management system with two main components:

1. **Todo Manager Sender**: A FastAPI application that allows users to input todos through the terminal
2. **Notification Logger**: A FastAPI service that receives webhooks and logs todos to a SQLite database

## Project Structure

```
.
├── notification_logger/
│   └── main.py         # Webhook receiver and database logger
├── todo_manager_sender/
│   └── send_todo.py    # Todo input and webhook sender
└── todos.db            # SQLite database (created automatically)
```

## Features

- Interactive todo input through terminal
- Webhook-based communication between services
- SQLite database logging of all todos
- REST API endpoints to view todos
- Automatic timestamp tracking
- Error handling and validation

## Setup and Installation

1. Install dependencies:
```bash
pip install fastapi uvicorn requests
```

2. Start the Notification Logger service:
```bash
uvicorn notification_logger.main:app --reload
```

3. Start the Todo Manager Sender:
```bash
uvicorn todo_manager_sender.send_todo:app --reload
```

## Usage

1. Open your browser and navigate to `http://localhost:8000` to start the todo input interface
2. Follow the prompts to enter todo details:
   - Enter a title (required)
   - Enter a description (optional)
3. The todo will be automatically sent to the webhook and logged in the database
4. View all todos by visiting `http://localhost:8000/todos`

## API Endpoints

### Notification Logger Service

- `POST /webhook/todo-added`: Receives todo webhooks
- `GET /todos`: Returns all logged todos
- `GET /`: Health check endpoint

### Todo Manager Sender

- `GET /`: Starts the todo input interface

## Data Model

```python
class Todo:
    id: int
    title: str
    description: Optional[str]
    created_at: datetime  # Automatically added by the logger
```

## Error Handling

- Input validation for todos
- Database operation error handling
- Webhook communication error handling
- User-friendly error messages 