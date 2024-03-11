# Import necessary modules
import os
from dotenv import load_dotenv
import asyncpg
from fastapi import FastAPI, Depends, HTTPException
from starlette.requests import Request

# Create a FastAPI instance
app = FastAPI()

# Load environment variables from a .env file
load_dotenv()

# Get the database secret from environment variables
db_secret = os.getenv("DB_SECRET")


# Define a connection manager class
class ConnectionManager:
    def __init__(self):
        # Initialize connection to None
        self.conn = None

    async def start(self):
        # Start the connection pool
        self.conn = await asyncpg.create_pool(dsn=db_secret)

    async def stop(self):
        # Close the connection pool
        await self.conn.close()

    async def get_conn(self):
        # Return the connection pool
        return self.conn


# Create a connection manager instance
conn_manager = ConnectionManager()


# Define a startup event handler
@app.on_event("startup")
async def startup():
    # Start the connection manager and set the connection pool in the app state
    await conn_manager.start()
    app.state.db = await conn_manager.get_conn()


# Define a shutdown event handler
@app.on_event("shutdown")
async def shutdown():
    # Stop the connection manager
    await conn_manager.stop()


# Define a dependency that gets the database connection from the app state
def get_db(request: Request):
    return request.app.state.db


# Define a route that reads from the database
@app.get("/")
async def read_root(db=Depends(get_db)):
    result = await db.fetch("select * from todo")
    return result


# Define a route that creates an item in the database
@app.post("/todo")
async def create_item(content: str, db=Depends(get_db)):
    await db.execute("INSERT INTO todo (content) VALUES ($1)", content)
    return {"status": "Item created"}


# Define a route that updates an item in the database
@app.put("/todo/{item_id}")
async def update_item(item_id: int, content: str, db=Depends(get_db)):
    updated_rows = await db.execute(
        "UPDATE todo SET content = $1 WHERE id = $2",
        content,
        item_id,
    )
    if updated_rows == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"status": "Item updated"}


# Define a route that deletes an item from the database
@app.delete("/todo/{item_id}")
async def delete_item(item_id: int, db=Depends(get_db)):
    deleted_rows = await db.execute("DELETE FROM todo WHERE id = $1", item_id)
    if deleted_rows == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"status": "Item deleted"}
