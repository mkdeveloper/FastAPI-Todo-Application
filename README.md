# FastAPI Todo Application

This is a simple Todo application built with FastAPI and asyncpg. It provides a RESTful API for managing todo items in a PostgreSQL database. The project uses Poetry for dependency management.

## Features

- **Connection Manager**: Manages the lifecycle of the database connection pool.
- **Database Dependency**: Injects the database connection into route handlers.
- **CRUD Operations**: Provides routes for creating, reading, updating, and deleting todo items.

## Routes

- `GET /`: Fetches all todo items from the database.
- `POST /todo`: Creates a new todo item in the database.
- `PUT /todo/{item_id}`: Updates a specific todo item in the database.
- `DELETE /todo/{item_id}`: Deletes a specific todo item from the database.

## Setup

1. Clone the repository.
2. Install Poetry if you haven't already.
3. Navigate to the project directory and install the dependencies using Poetry:
   ```bash
   poetry install
   ```
4. Set the `DB_SECRET` environment variable to your PostgreSQL connection string.
5. Run the application using Poetry:
   `bash
 poetry run uvicorn fastapi_todo.main:app
 `
   Please note that this application is a simple example and might need to be adjusted based on your specific needs.
