import os

import psycopg
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float


def get_connection():
    return psycopg.connect(
        host=os.getenv("DB_HOST", "db"),
        dbname=os.getenv("DB_NAME", "testdb"),
        user=os.getenv("DB_USER", "testuser"),
        password=os.getenv("DB_PASSWORD", "testpass"),
    )


@app.on_event("startup")
def initialize_database():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS items (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                price DOUBLE PRECISION NOT NULL
            )
        """)


@app.post("/items", status_code=201)
def create_item(item: Item):
    with get_connection() as conn:
        row = conn.execute(
            "INSERT INTO items (name, price) VALUES (%s, %s) RETURNING id",
            (item.name, item.price),
        ).fetchone()

    return {"id": row[0], **item.model_dump()}


@app.get("/items/{item_id}")
def get_item(item_id: int):
    with get_connection() as conn:
        row = conn.execute(
            "SELECT id, name, price FROM items WHERE id = %s",
            (item_id,),
        ).fetchone()

    if row is None:
        raise HTTPException(status_code=404, detail="Item not found")

    return {"id": row[0], "name": row[1], "price": row[2]}
